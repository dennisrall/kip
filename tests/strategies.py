import hypothesis.strategies as st
from hypothesis.strategies import SearchStrategy

from kip.models import Command


command: SearchStrategy[Command] = st.builds(Command, st.text(), st.text(), st.text())
command_set: SearchStrategy[set[Command]] = st.sets(command)
non_empty_command_set: SearchStrategy[set[Command]] = st.sets(command, min_size=1)
