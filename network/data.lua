--
-- Created by IntelliJ IDEA.
-- User: mlennox
-- Date: 14/06/2016
-- Time: 23:44
--

-- NOTE : this loads all images into memory and should not be used for very large datasets

require 'lfs'
require 'pprint'
require 'nn'
require 'image'

-- sadly, lfs - on OSX at least - does not provide attributes reliably
-- so we can't write a fool-proof way of loading just the folders
-- we'll have to assume (a good assumption though) that we can ignore
-- folder/files starting with '.'
local stupid_dir_check = function(dir_name)
    return string.sub(dir_name, 1, 1) ~= '.'
end

--function file_open(dir, file)
--    local path = dir .. "/" .. file
--    local fh = assert(io.open(path, "r"))
--    content = fh:read "*a"
--
--    fh:close()
--
--    return content
--end

local find_images = function(folder)
    imgs = {}
    count = 0
    for img in lfs.dir(folder) do
        if stupid_dir_check(img) then
            table.insert(imgs, img)
            count = count + 1
        end
    end
    return imgs, count
end

local load_images_from = function(folder, image_dim)
    print("folder",folder)
    print("image dimension",image_dim)
    local img_names, img_count = find_images(folder)
    local images = torch.Tensor(img_count,3, image_dim, image_dim)

    for i=0,img_count do
        print('img name : ', img_names[i+1])
        images[i+1] = image.load(folder..'/'..img_names[i+1])
--        file_open(folder,img_names[i+1])
    end

    return images
end



local load_dataset = function()
    image_dim = 32
    local data_split = {80,10,10} -- 80% train, 10% validation, 10% test

    data_dir = "../data/generated"
    local labels = {}
    local images = {}

    for dir in lfs.dir(data_dir) do
        local att = lfs.attributes(dir)

        if stupid_dir_check(dir) then
            table.insert(labels, dir)
            local class_images = load_images_from(data_dir..'/'..dir, image_dim)
            pprint(class_images)
        end
    end

--    pprint(labels)
--    pprint(images)
end

load_dataset()

return {
    load_dataset
}



