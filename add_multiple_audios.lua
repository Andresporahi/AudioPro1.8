-- ReaScript para agregar múltiples audios a sesión de Reaper
-- AudioPro v1.7 - Batch Processing Edition
-- Los archivos se colocan secuencialmente en el timeline

-- Obtener parámetros usando ExtState
local session_name = reaper.GetExtState("AudioPro", "session_name")
local template_path = reaper.GetExtState("AudioPro", "template_path")
local audio_files_list = reaper.GetExtState("AudioPro", "audio_files_list") -- Lista separada por "|"
local output_names_list = reaper.GetExtState("AudioPro", "output_names_list") -- Nombres originales separados por "|"
local session_dir = reaper.GetExtState("AudioPro", "session_dir") -- Directorio de salida

-- Debug: log de parámetros
reaper.ShowConsoleMsg("=== AudioPro v1.7 - Batch Processing ===\n")
reaper.ShowConsoleMsg("Session name: " .. session_name .. "\n")
reaper.ShowConsoleMsg("Template: " .. template_path .. "\n")
reaper.ShowConsoleMsg("Session dir: " .. session_dir .. "\n")
reaper.ShowConsoleMsg("Audio files: " .. audio_files_list .. "\n")
reaper.ShowConsoleMsg("Output names: " .. output_names_list .. "\n")

if audio_files_list == "" or session_name == "" or template_path == "" then
    reaper.MB("Error: Faltan parámetros", "AudioPro Error", 0)
    return
end

-- Verificar que el template existe
if not reaper.file_exists(template_path) then
    reaper.MB("Error: Template no encontrado: " .. template_path, "AudioPro Error", 0)
    return
end

-- Parsear lista de archivos y nombres
local function split_string(inputstr, sep)
    local t = {}
    for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
        table.insert(t, str)
    end
    return t
end

local audio_files = split_string(audio_files_list, "|")
local output_names = split_string(output_names_list, "|")

reaper.ShowConsoleMsg("Total de archivos a procesar: " .. #audio_files .. "\n")

-- Verificar que todos los archivos existen
for i, audio_file in ipairs(audio_files) do
    if not reaper.file_exists(audio_file) then
        reaper.MB("Error: Archivo no existe: " .. audio_file, "AudioPro Error", 0)
        return
    end
    
    -- Validar formato WAV
    local file = io.open(audio_file, "rb")
    if file then
        local size = file:seek("end")
        file:seek("set", 0)
        local riff = file:read(4)
        local file_size = file:read(4)
        local wave = file:read(4)
        file:close()
        
        reaper.ShowConsoleMsg(i .. ") " .. audio_file .. " - " .. size .. " bytes\n")
        
        if size < 1000 then
            reaper.MB("Error: Archivo " .. i .. " está vacío: " .. size .. " bytes", "AudioPro Error", 0)
            return
        end
        
        if riff ~= "RIFF" or wave ~= "WAVE" then
            reaper.MB("Error: Archivo " .. i .. " no es WAV válido", "AudioPro Error", 0)
            return
        end
    else
        reaper.MB("Error: No se pudo abrir archivo " .. i, "AudioPro Error", 0)
        return
    end
end

-- Cargar template
reaper.Main_openProject(template_path)
reaper.defer(function() end)

-- Guardar sesión con el nuevo nombre
reaper.ShowConsoleMsg("Guardando sesión como: " .. session_name .. "\n")
reaper.Main_SaveProjectEx(0, session_name, 0)

if not reaper.file_exists(session_name) then
    reaper.MB("Error: No se pudo guardar la sesión", "AudioPro Error", 0)
    return
end

-- Buscar la pista "Clase"
local track = nil
local track_count = reaper.CountTracks(0)

reaper.ShowConsoleMsg("Buscando pista 'Clase'...\n")
reaper.ShowConsoleMsg("Total de pistas: " .. track_count .. "\n")

for i = 0, track_count - 1 do
    local current_track = reaper.GetTrack(0, i)
    local _, track_name = reaper.GetSetMediaTrackInfo_String(current_track, "P_NAME", "", false)
    
    if track_name:lower() == "clase" then
        track = current_track
        reaper.ShowConsoleMsg("¡Pista 'Clase' encontrada!\n")
        break
    end
end

if not track then
    reaper.MB("Error: No se encontró la pista 'Clase'", "AudioPro Error", 0)
    return
end

-- Seleccionar la pista
reaper.SetOnlyTrackSelected(track)
reaper.SetTrackSelected(track, true)

-- Insertar todos los archivos secuencialmente
local current_position = 0
local total_duration = 0
local items_info = {} -- Guardar info de cada ítem para los renders individuales

reaper.ShowConsoleMsg("\n=== Insertando archivos en timeline ===\n")

for i, audio_file in ipairs(audio_files) do
    reaper.ShowConsoleMsg("\nInsertando archivo " .. i .. "/" .. #audio_files .. "...\n")
    reaper.ShowConsoleMsg("Archivo: " .. audio_file .. "\n")
    reaper.ShowConsoleMsg("Posición: " .. current_position .. " segundos\n")
    
    -- Crear ítem
    local item = reaper.AddMediaItemToTrack(track)
    
    if item then
        -- Crear source desde archivo
        local pcm_source = reaper.PCM_Source_CreateFromFile(audio_file)
        
        if pcm_source then
            local source_length = reaper.GetMediaSourceLength(pcm_source)
            reaper.ShowConsoleMsg("Duración: " .. source_length .. " segundos\n")
            
            if source_length > 0 then
                -- Crear take y asignar source
                local take = reaper.AddTakeToMediaItem(item)
                reaper.SetMediaItemTake_Source(take, pcm_source)
                
                -- Configurar posición y duración
                reaper.SetMediaItemInfo_Value(item, "D_POSITION", current_position)
                reaper.SetMediaItemInfo_Value(item, "D_LENGTH", source_length)
                
                -- Actualizar ítem
                reaper.UpdateItemInProject(item)
                
                -- Guardar info para renders individuales
                local output_name = output_names[i] or ("audio_" .. i)
                table.insert(items_info, {
                    start_pos = current_position,
                    end_pos = current_position + source_length,
                    output_name = output_name
                })
                
                -- Actualizar posición para el siguiente archivo
                current_position = current_position + source_length
                total_duration = total_duration + source_length
                
                reaper.ShowConsoleMsg("✓ Insertado exitosamente\n")
            else
                reaper.MB("Error: Archivo " .. i .. " tiene duración 0", "AudioPro Error", 0)
                return
            end
        else
            reaper.MB("Error: No se pudo crear PCM_Source para archivo " .. i, "AudioPro Error", 0)
            return
        end
    else
        reaper.MB("Error: No se pudo crear ítem para archivo " .. i, "AudioPro Error", 0)
        return
    end
end

reaper.ShowConsoleMsg("\n=== Todos los archivos insertados ===\n")
reaper.ShowConsoleMsg("Duración total del timeline: " .. total_duration .. " segundos\n")

-- Guardar sesión con todos los ítems
reaper.Main_SaveProjectEx(0, session_name, 0)

-- Crear carpeta "procesados" si no existe
local procesados_dir = session_dir .. "\\procesados"
local mkdir_cmd = 'mkdir "' .. procesados_dir .. '" 2>nul'
os.execute(mkdir_cmd)
reaper.ShowConsoleMsg("Carpeta de salida: " .. procesados_dir .. "\n")

-- Renderizar cada archivo individualmente
reaper.ShowConsoleMsg("\n=== Iniciando renders individuales ===\n")

for i, info in ipairs(items_info) do
    reaper.ShowConsoleMsg("\nRenderizando " .. i .. "/" .. #items_info .. ": " .. info.output_name .. "\n")
    
    -- Configurar time selection para este segmento
    reaper.GetSet_LoopTimeRange(true, false, info.start_pos, info.end_pos, false)
    
    -- Configurar archivo de salida
    local output_file = procesados_dir .. "\\" .. info.output_name .. "_procesado.wav"
    reaper.ShowConsoleMsg("Output: " .. output_file .. "\n")
    
    -- Configurar render
    reaper.GetSetProjectInfo_String(0, "RENDER_FILE", output_file, true)
    reaper.GetSetProjectInfo(0, "RENDER_SRATE", 48000, true) -- 48kHz
    reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 1, true) -- Mono
    
    -- WAV 24-bit PCM
    local wav_cfg = "ZXZhdxgAAAA="
    reaper.GetSetProjectInfo_String(0, "RENDER_FORMAT", wav_cfg, true)
    
    -- Source: Master mix
    reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", 0, true)
    
    -- Bounds: Time selection
    reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 1, true)
    
    -- Tail: 1000ms
    reaper.GetSetProjectInfo(0, "RENDER_TAILFLAG", 1, true)
    reaper.GetSetProjectInfo(0, "RENDER_TAILMS", 1000, true)
    
    -- Resample mode
    reaper.GetSetProjectInfo(0, "RENDER_RESAMPLE", 2, true)
    
    -- Guardar antes de renderizar
    reaper.Main_SaveProjectEx(0, session_name, 0)
    
    -- Ejecutar render
    reaper.Main_OnCommand(41824, 0)
    
    -- Esperar a que el render termine
    local timeout = 60 -- 60 segundos máximo por archivo
    local elapsed = 0
    while elapsed < timeout do
        if reaper.file_exists(output_file) then
            -- Verificar que el archivo tenga tamaño
            local check_file = io.open(output_file, "rb")
            if check_file then
                local size = check_file:seek("end")
                check_file:close()
                if size > 1000 then
                    reaper.ShowConsoleMsg("✓ Render completado (" .. size .. " bytes)\n")
                    break
                end
            end
        end
        
        -- Esperar 500ms
        local wait_start = reaper.time_precise()
        while reaper.time_precise() - wait_start < 0.5 do
            -- Busy wait
        end
        elapsed = elapsed + 0.5
    end
    
    if elapsed >= timeout then
        reaper.ShowConsoleMsg("⚠ Timeout esperando render de " .. info.output_name .. "\n")
    end
end

reaper.ShowConsoleMsg("\n=== Proceso completado exitosamente ===\n")
reaper.ShowConsoleMsg("Archivos procesados: " .. #items_info .. "\n")
reaper.ShowConsoleMsg("Ubicación: " .. procesados_dir .. "\n")
reaper.ShowConsoleMsg("\nReaper permanecerá abierto para revisar el resultado\n")

