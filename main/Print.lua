-- Put functions in this file to use them in several other scripts.
-- To get access to the functions, you need to put:
-- require "my_directory.my_file"
-- in any script using the functions.
function Print(debug, ...)
	if debug then
		local args = {...}
		local msg = table.concat(args, " ")  -- Concatenate all arguments with a space
		print(msg)
	end
end
