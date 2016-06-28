--
-- Created by IntelliJ IDEA.
-- User: mlennox
-- Date: 16/06/2016
-- Time: 00:23
--

local data = require "./data"

local dataset = data.load_dataset()

for k, v in pairs( dataset ) do
    print(k, v)
end


