cc.FileUtils:getInstance():setPopupNotify(false)

local writePath = cc.FileUtils:getInstance():getWritablePath()
local resSearchPaths = {
	writePath,
	writePath .. "src/",
	writePath .. "src/",
	writePath .. "res/sd/",
	writePath .. "res/",
	"src/",
	"src/",
	"res/sd/",
	"res/"
}
cc.FileUtils:getInstance():setSearchPaths(resSearchPaths)

require "config"
require "cocos.init"

local function main()
    require("app.MyApp"):create():run()
end

--local function main()
--    local msgToSend = {}
--    openId = "oL5RGwKaeIeQlNVk3eGCuJPmJqqs"
--	accessToken = "Xux2XXNGizw340jag9H_MzAS5r3ieWoPFILwwp-dSDSJB3XamwLFaZcFckloO779rYBl0i2DOPi2KCn9eRP78aQnE-Rvi2emYkDEZrgGoDw"
--	refreshToken = "xsAgfCbmE_Qv-co73npuMitr67y4hiTFAuO7zckCB5CeSd0ahogvJZlcCZc89YJxayzbfXrmH0Rtw-DBUKe4UsLi6Z034FQZQIohHjxOd0A"
--	unionid = "ohEZ3w5DUA7yONoq9U7moFSktWhs"
--	local catStr = string.format("%s%s%s%s", openId, accessToken, refreshToken, unionid)
--	msgToSend.m_md5 = cc.UtilityExtension:generateMD5(catStr, string.len(catStr))
--end

local status, msg = xpcall(main, __G__TRACKBACK__)
if not status then
    print(msg)
end
