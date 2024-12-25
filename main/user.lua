-- Put functions in this file to use them in several other scripts.
-- To get access to the functions, you need to put:
-- require "my_directory.my_file"
-- in any script using the functions.
local M = {}

-- all users of the module will share this table
local state = {}

function M.do_something(foobar)
	table.insert(state, foobar)
end

return M