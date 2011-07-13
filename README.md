A very simple IRC bot used by #ec09 @ FreeNode.

Simple use cases
----------------

- Adding a command
    Write a callable in commands/<command\_name>.py and add <command\_name> to
command\_modules in commands/\_\_init\_\_.py.

    The command name, callable and aliases should be declared in a list
or tuple called command\_description in commands/<command\_name>.py

    The callable receives as argument the EC09Bot instance.

- Removing a command
    Simply remove the command module's name from command\_modules in
commands/\_\_init\_\_.py.
