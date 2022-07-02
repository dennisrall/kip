import hypothesis.strategies as st

from src.command import Command


command = st.builds(Command, st.text(), st.text(), st.text())
command_set = st.sets(command)
non_empty_command_set = st.sets(command, min_size=1)
