from pathlib import Path
from importlib import resources


def get_example_inputs(day: int) -> tuple[tuple[str, str], ...]:
    package_dir = resources.files(__package__)
    base_dir = Path(str(package_dir)).joinpath('static', 'inputs')
    
    def split_input_output(input_file: Path) -> tuple[str, str]:
        input_, output = input_file.read_text().split("\n\n")
        return (input_.strip(), output.strip())

    return tuple(
        split_input_output(input_file)
        for input_file in base_dir.glob(f"example.day.{day}.*")
    )
