A very simple IRC bot used by #ec09 @ FreeNode.

Simple usage
------------

- Adding a command

    Write a callable in commands/\<command\_name\>.py and add \<command\_name\>
to command\_modules in commands/\_\_init\_\_.py. This callable will get called
when a user requests your command.

    The command name, callable and aliases should be declared in a global
variable called *command\_description* in commands/\<command\_name\>.py. It
should be an iterable of tuples (*command name*, *callable*, *aliases*), where
*aliases* is an iterable of aliases.

    Thus in the common case in which your file defines a single command,
a declaration like:

    ```python
    command_description = [("foo", foobar, ("bar, "baz"))]
    ```

    suffices to declare a command "foo", with aliases "bar" and "baz". That is,
the callable foobar gets called when a user issues either !foo, !bar or !baz.

    The callable receives as argument the EC09Bot instance. If its return value
is not None, it is sent back as a direct message to the calling user.

    A special case for this is adding a fortune command (that is, a command
that returns a fortune cookie). These are all defined in commands/fortune.py,
just add your command there and it will show up among the other commands.

- Removing a command

    Simply remove the command module's name from command\_modules in
commands/\_\_init\_\_.py.

    Fortune commands are once again an exception. Remove the command from
commands/fortune.py in order to disable it.
