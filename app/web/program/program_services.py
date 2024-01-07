import os

from dotenv import load_dotenv
from dependency_injector import containers, providers

load_dotenv('.env')


class ProgramServices(containers.DeclarativeContainer):
    """Container with the program service"""
    
    program_type = os.environ.get('PROGRAM_TYPE', 'flask')

    if program_type == 'print':
        from .print_program import PrintProgram
        program = providers.Factory(PrintProgram)

    elif program_type == 'flask':
        from .flask_program import FlaskProgram
        program = providers.Factory(FlaskProgram)
        
    else:
        raise ValueError(f"Invalid PROGRAM_TYPE: {program_type}")
    