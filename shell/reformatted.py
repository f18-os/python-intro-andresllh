#!usr/bin/env python3
import sys
import re
import os
import subprocess



def main():
    while(True):
        arg = input(os.environ['PS1'] + '$')
        if "/bin/" in arg:
            arg = arg.replace("/bin/", "")
        
        if arg == 'exit':
            return
        
        if "cd" in arg:
            args = arg.split()
            
            if args[0].strip() == "cd":
                if len(args) < 2:
                    continue
                if args[1].strip() == "..":
                    curr = os.getcwd()
                    next_dir = curr.rsplit('/', 1)[0]
                    os.chdir(next_dir)
                    continue
                else:
                    os.chdir(args[1].strip())
                    continue
        
        elif arg == '':
            continue
        
        
        else:
            pid = os.getpid() 
            if '|' in arg:
                pipe(arg)
                        
 
            elif '>' in arg:
                redirect_output(arg)

                          
                          
            elif '<' in arg:
                redirect_input(arg)
        
        
            else:
                execute_command(arg)


def execute_command(arg):
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
    return

def pipe(arg):
    rc = os.fork()
    import fileinput
    print("About to fork (pid=%d)" % pid)
    args = arg.split()
    if rc == 0:
        pr, pw= os.pipe()
        for f in (pr, pw):
            os.set_inheritable(f, True)
        pc = os.fork()
        if pc == 0:
            os.close(1) 
            os.dup(pw)
            os.set_inheritable(1, True)
            for fd in (pr, pw):
                os.close(fd)
            f_args = [args[0], args[1]]
            for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                program = "%s/%s" % (dir, args[0])
                try:
                    # error of bad file descriptor here
                    os.execve(program, f_args, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass
        else:
            os.close(0)
            os.dup(pr)
            os.set_inheritable(0, True)
            for fd in (pr, pw):
                os.close(fd)
            s_args = [args[3]]
            for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                program = "%s/%s" % (dir, args[3])
                try:
                    # error of bad file descriptor here
                    os.execve(program, s_args, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass
    else:
        childPidCode = os.wait()
    return


def redirect_input(arg):
    print('redirecting input')
    rc = os.fork()
    if rc == 0:
        os.close(0)                 # redirect child's stdin
        args = arg.split()
        sys.stdin = open(args[1], "w")
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
    
    return

                                
def redirect_output(arg):
    print('redirecting output')
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
    return
    

os.environ['PS1'] = ''                    
main()
        
