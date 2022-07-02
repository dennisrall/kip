import os

from kip.services.run_command import run_command


def test_run_command_mock(ls_command, mocker):
    os_system_mock = mocker.Mock()
    mocker.patch.object(os, "system", os_system_mock)
    run_command(ls_command)
    os_system_mock.assert_called_with(ls_command.command)
