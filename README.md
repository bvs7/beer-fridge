# beer-fridge
Use a raspberry pi to regulate a fridge temperature

To run using tmux:

`tmux new -s Fridge`

To check if this is running using tmux:

`tmux list-sessions | grep Fridge`

To check status of the run:

`tmux attach -t Fridge`

(`-t Fridge` is optional if only one tmux session is running)

To leave a tmux session, press `ctrl-b`, release, then press `d`
