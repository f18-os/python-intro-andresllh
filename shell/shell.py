#!usr/bin/env python3
import sys
import re
import os
import subprocess



def main():
    while(True):
        arg = input(os.environ['PS1'] + '$')
        if arg == 'exit':
            return
        
        elif arg == '':
            continue

        else:
            pid = os.getpid() 
            if '|' in arg:
                pr,pw = os.pipe()
                rc = os.fork()
                for f in (pr, pw):
                    os.set_inheritable(f, True)
                
                print("pipe fds: pr=%d, pw=%d" % (pr, pw))

                import fileinput
                print("About to fork (pid=%d)" % pid)
                args = arg.split()
                if rc == 0:
                    os.close(1) 
                    os.dup(pw)
 
                    for fd in (pr, pw):
                        os.close(fd)
                                            
                    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                        program = "%s/%s" % (dir, args[0])
                        try:
                            # error of bad file descriptor here
                            os.execve(program, args, os.environ) # try to exec program
                        except FileNotFoundError:             # ...expected
                            pass
                    
                else:                           # parent (forked ok)
                    childPidCode = os.wait()
                    print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
                    os.close(0)
                    os.dup(pr) # is it the output of the first part of the pipe?
                    for fd in (pw, pr):
                        os.close(fd)
                    rc = os.fork()
                    if rc == 0:
                        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                            program = "%s/%s" % (dir, args[3])
                            try:
                                os.execve(program, args, os.environ) # try to exec program
                            except FileNotFoundError:             # ...expected
                                pass
                            
                    else:
                        childPidCode = os.wait()
                        
                    #for line in fileinput.input():
                        #print("From child: <%s>" % line)
            elif '>' in arg:
                print('redirecting output')
                print(arg.split())
                rc = os.fork()
                if rc == 0:
                    os.close(1)                 # redirect child's stdout
                    args = arg.split()
                    sys.stdout = open(args[-1], "w")
                    os.set_inheritable(1, True)
                    for dir in re.split(":", os.environ['PATH']): # try each directory in path
                        program = "%s/%s" % (dir, args[0])
                        try:
                            os.execve(program, args, os.environ) # try to exec program
                        except FileNotFoundError:             # ...expected
                            pass    
                    sys.exit(1)                 # terminate with error
                else:                           # parent (forked ok)
                    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                                (pid, rc)).encode())
                    childPidCode = os.wait()

                                
            elif '<' in arg:
                print('redirecting input')
                rc = os.fork()
                if rc == 0:
                    os.close(0)                 # redirect child's stdin
                    args = arg.split()
                    sys.stdin = open(args[2], "w")
                    os.set_inheritable(0, True)                    
                    for dir in re.split(":", os.environ['PATH']): # try each directory in path
                        program = "%s/%s" % (dir, args[0])
                        try:
                            os.execve(program, args, os.environ) # try to exec program
                        except FileNotFoundError:             # ...expected
                            pass                              # ...fail quietly 
                    
                    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
                    sys.exit(1)                 # terminate with error
                
                else:                         # parent (forked ok)
                    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                                (pid, rc)).encode())
                    childPidCode = os.wait()
                    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                                childPidCode).encode())
        
            else:
                rc = os.fork()
                if rc == 0:
                    args = arg.split()
                    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                        program = "%s/%s" % (dir, args[0])
                        try:
                            os.execve(program, args, os.environ) # try to exec program
                        except FileNotFoundError:             # ...expected
                            pass
                            
                else:                           # parent (forked ok)
                    #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                     #           (pid, rc)).encode())
                    childPidCode = os.wait()
                    #os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                                #childPidCode).encode())

os.environ['PS1'] = ''                    
main()
        