import tqdm
import argparse

def start(num_users, base_dir='./', session_name = "my_session"):
    server = libtmux.Server()
    if (server.has_session(session_name)):
        print('Error: session already exists')
		return
    session = server.new_session(session_name)
    for i in tqdm.tqdm(range(num_users)):
        work_directory = base_dir + str(i)
        port = 20000 + i
        token = "token: " + str(i)
        window = session.new_window(window_name = str(i), attach = False)
        pane = window.attached_pane
        pane.send_keys("jupyter notebook â€â€”port %d â€â€”no-browser â€â€”NotebookApp.token=%s â€â€”NotebookApp.notebook_dir=%s" %(port, str(token), work_directory), enter=True)
    

def stop(session_name, num):
    server = libtmux.Server()
    if (!server.has_session(session_name)):
	    print('Error: session not found')
		return
    session = server.find_where({"session_name" : session_name})
    window = session.find_where({"window_name" : str(num)})
    window.kill_window()

def stop_all(session_name):
    server = libtmux.Server()
    if (!server.has_session(session_name)):
        print('Error: session not found')
		return
    server.kill_session(session_name)

parser = argparse.ArgumentParser()
parser.add_argument("command", help = "use start, stop or stop_all")
parser.add_argument(nargs = '+', dest = "function_arguments")
arguments = parser.parse_args()

function_arguments_len = len(arguments.function_arguments)

f_arg = arguments.function_arguments[0]
s_arg = None
t_arg = None
if function_arguments_len == 2:
    s_arg = arguments.function_arguments[1]
if function_arguments_len == 3:
    t_arg = arguments.function_arguments[2]

if arguments.command == "start":
    if function_arguments_len == 3:   
        start(f_arg, s_arg, t_arg)
    elif function_arguments_len == 2:
        start(f_arg, s_arg)
    else:  
        start(f_arg)
elif arguments.command == "stop":
    stop(f_arg, int(s_arg))
elif arguments.command == "stop_all":
    stop_all(f_arg)
else:
    print("Error: Argument not found")
