-- ReaScript para agregar múltiples audios/videos a sesión de Reaper
-- AudioPro v1.8 - Batch Processing con Video Support
-- Los archivos se colocan secuencialmente en el timeline

-- Obtener parámetros usando ExtState
local session_name = reaper.GetExtState("AudioPro", "session_name")
local template_path = reaper.GetExtState("AudioPro", "template_path")
local media_files_list = reaper.GetExtState("AudioPro", "audio_files_list") -- Archivos (audio o video)
local output_names_list = reaper.GetExtState("AudioPro", "output_names_list") -- Nombres originales
local session_dir = reaper.GetExtState("AudioPro", "session_dir") -- Directorio de salida

-- Debug: log de parámetros
reaper.ShowConsoleMsg("=== AudioPro v1.8 - Media Batch Processing ===\n")
reaper.ShowConsoleMsg("Session name: " .. session_name .. "\n")
reaper.ShowConsoleMsg("Template: " .. template_path .. "\n")
reaper.ShowConsoleMsg("Session dir: " .. session_dir .. "\n")
reaper.ShowConsoleMsg("Media files: " .. media_files_list .. "\n")
reaper.ShowConsoleMsg("Output names: " .. output_names_list .. "\n")

if media_files_list == "" or session_name == "" or template_path == "" then
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

-- Detectar si un archivo es video
local function is_video_file(filepath)
    local ext = string.lower(string.match(filepath, "%.([^%.]+)$") or "")
    local video_exts = {mp4=true, avi=true, mov=true, mkv=true, wmv=true, flv=true, webm=true}
    return video_exts[ext] == true
end

local media_files = split_string(media_files_list, "|")
local output_names = split_string(output_names_list, "|")

reaper.ShowConsoleMsg("Total de archivos a procesar: " .. #media_files .. "\n")

-- Verificar que todos los archivos existen
local has_video = false
for i, media_file in ipairs(media_files) do
    if not reaper.file_exists(media_file) then
        reaper.MB("Error: Archivo no existe: " .. media_file, "AudioPro Error", 0)
        return
    end
    
    local is_video = is_video_file(media_file)
    if is_video then
        has_video = true
        reaper.ShowConsoleMsg(i .. ") 🎬 VIDEO: " .. media_file .. "\n")
    else
        reaper.ShowConsoleMsg(i .. ") 🎵 AUDIO: " .. media_file .. "\n")
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

for i, media_file in ipairs(media_files) do
    reaper.ShowConsoleMsg("\nInsertando archivo " .. i .. "/" .. #media_files .. "...\n")
    reaper.ShowConsoleMsg("Archivo: " .. media_file .. "\n")
    reaper.ShowConsoleMsg("Posición: " .. current_position .. " segundos\n")
    
    -- Crear ítem
    local item = reaper.AddMediaItemToTrack(track)
    
    if item then
        -- Crear source desde archivo (funciona para audio y video)
        local pcm_source = reaper.PCM_Source_CreateFromFile(media_file)
        
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
                local output_name = output_names[i] or ("media_" .. i)
                local is_video = is_video_file(media_file)
                local output_ext = is_video and string.match(media_file, "%.([^%.]+)$") or "wav"
                
                table.insert(items_info, {
                    start_pos = current_position,
                    end_pos = current_position + source_length,
                    output_name = output_name,
                    is_video = is_video,
                    extension = output_ext
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
            reaper.MB("Error: No se pudo crear source para archivo " .. i, "AudioPro Error", 0)
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
    
    -- Configurar archivo de salida según el tipo
    local output_file
    if info.is_video then
        output_file = procesados_dir .. "\\" .. info.output_name .. "_procesado." .. info.extension
        reaper.ShowConsoleMsg("🎬 Renderizando VIDEO\n")
    else
        output_file = procesados_dir .. "\\" .. info.output_name .. "_procesado.wav"
        reaper.ShowConsoleMsg("🎵 Renderizando AUDIO\n")
    end
    
    reaper.ShowConsoleMsg("Output: " .. output_file .. "\n")
    
    -- Configurar render
    reaper.GetSetProjectInfo_String(0, "RENDER_FILE", output_file, true)
    reaper.GetSetProjectInfo(0, "RENDER_SRATE", 48000, true) -- 48kHz
    
    if info.is_video then
        -- Configuración para VIDEO
        reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 2, true) -- Stereo para video
        
        -- Video render settings
        -- Activar video rendering
        local video_config = reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", 0, false)
        -- Bit 2 = include video
        video_config = video_config | 2
        reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", video_config, true)
        
        -- MP4/Video format (según extensión)
        if info.extension == "mp4" then
            -- MP4 format
            local mp4_cfg = "bDRtcBAAAAA="  -- Base64 para MP4
            reaper.GetSetProjectInfo_String(0, "RENDER_FORMAT", mp4_cfg, true)
        end
    else
        -- Configuración para AUDIO solo
        reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 1, true) -- Mono
        
        -- WAV 24-bit PCM
        local wav_cfg = "ZXZhdxgAAAA="
        reaper.GetSetProjectInfo_String(0, "RENDER_FORMAT", wav_cfg, true)
    end
    
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
    local timeout = 120 -- 120 segundos máximo por archivo (videos pueden tardar más)
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

