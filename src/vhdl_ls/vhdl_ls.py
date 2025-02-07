from simplhdl.flow import FlowBase, FlowFactory

from simplhdl.pyedaa.fileset import FileSet
from simplhdl.pyedaa import HDLSourceFile, SourceFile, ConstraintFile
from simplhdl.pyedaa.project import Project

from argparse import Namespace
from pathlib import Path
import jinja2

PROGNAME = "vhdl_ls"

TEMPLATE = """
# This file is autogenerated
# VHDL-LS project configuration file

standard = "2008"

[libraries]
{% for lib, files in libs.items() -%}
    {{ lib }}.files = [
        {% for file in files -%}
            '{{ file }}',
        {% endfor %}
    ]
{% endfor %}
"""

#{% for lib in ext_libs -%}
#    {{ lib.Name }}.is_third_party = true
#{% endfor %}

def get_libraries(project):
    s = set()
    libs = {}
    for file in project.DefaultDesign.Files():
        if isinstance(file, HDLSourceFile):
            lib = str(file.Library)
            path = str(file.Path)
            file_id = f"{lib}:{path}"
            if file_id in s:
                continue
            s.add(file_id)
            if not lib in libs:
                libs[lib] = []
            libs[lib].append(path)

    return libs

def get_external_libraries(project):
    libs = []
    for resource in project.DefaultDesign.ExternalVHDLLibraries.values():
        libs.append(resource)
    return libs

def print_libraries(libs):
    for lib in libs.keys():
        print(f"[{lib}]")
        for file in libs[lib]:
            print(f"{file}")
        print("")

def generate_config_file(project):
    template = jinja2.Template(TEMPLATE)
    libs = get_libraries(project)
    ext_libs = get_external_libraries(project)
    output = template.render(libs=libs, ext_libs=ext_libs)
    return output

@FlowFactory.register(PROGNAME)
class VhdlLsFlow(FlowBase):
    def __init__(self, name: str, args: Namespace, project: Project, builddir: Path):
        super().__init__(name, args, project, builddir)

    @classmethod
    def parse_args(cls, subparsers):
        parser = subparsers.add_parser(PROGNAME, help="Generate VHDL_LS configuration (.vhdl_ls.toml)")

    def run(self):
        #libs = get_libraries(self.project)
        #print_libraries(libs)
        cfg_file = generate_config_file(self.project)
        print(cfg_file)

