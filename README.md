A very simple IRC bot used by #ec09 @ FreeNode.

Simple use cases
----------------

- Adding a command
Write a callable in commands/<command_name>.py and add <command_name> to
command_modules in commands/__init__.py.
The command name, callable and aliases should be declared in a list
or tuple called command_description in commands/<command_name>.py
The callable receives as argument the EC09Bot instance.

- Removing a command
Simply remove the command module's name from command_modules in
commands/__init__.py.
