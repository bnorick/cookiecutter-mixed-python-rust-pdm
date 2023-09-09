import pathlib

from setuptools import setup
from setuptools_rust import Binding, RustExtension

# create target dir to store annoying .egg-info directory
(pathlib.Path(__file__).parent / "target").mkdir(exist_ok=True)

setup(
    name="{{ cookiecutter.package_name }}",
    rust_extensions=[
        RustExtension(
            "{{ cookiecutter.package_name }}._{{ cookiecutter.package_name }}",
            binding=Binding.PyO3,
            debug=False,
        )
    ],
    package_data={"{{ cookiecutter.package_name }}": ["py.typed"]},
    packages=["{{ cookiecutter.package_name }}"],
    package_dir={"{{ cookiecutter.package_name }}": "src/python/{{ cookiecutter.package_name }}"},
    zip_safe=False,
)
