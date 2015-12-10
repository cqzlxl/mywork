##-*-coding: utf-8;-*-##
import cmd
import os


class Control(cmd.Cmd):
    supported_sh_cmd = (
        'man',
        'help',
        'ls',
        'cat',
        'ssh',
        'find',
        'tail',
        'xargs',
        'grep'
    )


    def emptyline(self):
        pass


    def do_exit(self, line):
        self._do_exit(line)

    def help_exit(self):
        self._print_leave_help_message('exit')


    def do_EOF(self, line):
        print
        self._do_exit(line)
        return True

    def help_EOF(self):
        self._print_leave_help_message('EOF')


    def do_shell(self, line):
        if self._is_sh_cmd_safe(line):
            os.system(line)
        else:
            self.default(line)

    def help_shell(self):
        self.usage('shell', '<command line>.', 'Execute shell commands')
        print 'You can also use the ! shortcut.'


    def do_logging(self, line):
        pass

    def help_logging(self):
        self.usage('logging', '<level> [logger]', 'Change the server logging policy.')


    def usage(self, cmd, args, desc):
        print 'Usage:', cmd, args
        print desc
        print


    def _is_sh_cmd_safe(self, line):
        c = line.split()[0]
        if c not in self.supported_sh_cmd:
            return False

        if '|' in line:
            return False

        if '>' in line:
            return False

        if '>>' in line:
            return False

        if '&' in line:
            return False

        return True


    def _do_exit(self, line):
        print 'Bye'
        exit(0)


    def _print_leave_help_message(self, cmd):
        if cmd == 'EOF':
            other = 'exit'
        else:
            other = 'EOF'
        self.usage(cmd, '', 'Exit the controller.')
        print 'You can also use the {} command or Ctrl-D shortcut.'.format(other)


if __name__ == '__main__':
    interpreter = Control()
    interpreter.prompt = 'Server admin> '
    interpreter.cmdloop()
