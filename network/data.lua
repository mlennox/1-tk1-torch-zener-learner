--
-- Created by IntelliJ IDEA.
-- User: mlennox
-- Date: 14/06/2016
-- Time: 23:44
--

require 'lfs'
require 'pprint'
require 'nn'

function file_open(dir, file)
    local path = dir .. "/" .. file
    local fh = assert(io.open(path, "r"))
    local content = fh:read "*a"

    fh:close()

    return content
end

local load_images_from = function(folder)
    local images = {}

    for img in lfs.dir(folder) do
        if string.sub(img, 1, 1) ~= '.' then
            table.insert(images, file_open(folder,img))
        end
    end

    return images
end

local load_dataset = function()
    local data_dir = "../data/generated/"
    local labels = {}
    local images = {}

    for dir in lfs.dir(data_dir) do
        if string.sub(dir, 1, 1) ~= '.' then
            table.insert(labels, dir)
            table.insert(images, load_images_from(data_dir..'/'..dir))
        end
    end

--    pprint(labels)
--    pprint(images)
end

load_dataset()



