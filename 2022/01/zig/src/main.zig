const std = @import("std");
const fs = std.fs;

pub fn main() !void {
    std.debug.print("Hello, World!", .{});

    const fname = "/home/gadokrisztian/git/advent-of-code-soultions/2022/01/zig/input.txt";
    var f = try fs.cwd().openFile(fname, fs.File.OpenMode{ .Read = {} });
    defer f.close();

    const stdout = std.io.getStdOut().writer();

    var buf: [std.mem.page_size]u8 = undefined;

    var bytes_read = try f.read(&buf);
    while (bytes_read > 0) {
        try stdout.print("{}**", .{buf[0..bytes_read]});
        bytes_read = try f.read(&buf);
    }
}
