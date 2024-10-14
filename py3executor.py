import json
import os
import sys
from typing import Callable

def fail():
    exit(-1)

class Flow:
    __variables = {}
    __export_vars = {}
    __inited = False

    @staticmethod
    def init_variables(variables: dict):
        if Flow.__inited:
            return
        Flow.__variables = variables
        Flow.__inited = True

    @staticmethod
    def get_variable(key: str, force: bool=False) -> str | None:
        if key not in Flow.__variables:
            if force:
                print(f"Flow variable {key} not found")
                fail()
            return None
        return Flow.__variables[key]

    @staticmethod
    def set_export_var(key: str, value: str):
        Flow.__export_vars[key] = value

    @staticmethod
    def del_export_var(key: str):
        if key in Flow.__export_vars:
            del Flow.__export_vars[key]

    @staticmethod
    def export_vars() -> dict:
        return Flow.__export_vars

class Helper:
    __args = {}
    __inited = False

    @staticmethod
    def init_args(args: dict):
        if Helper.__inited:
            return
        Helper.__args = args
        Helper.__inited = True

    @staticmethod
    def get_arg(key: str, force: bool=False) -> str|None:
        if key not in Helper.__args:
            if force:
                print(f"Helper argument {key} not found")
                fail()
            return None
        return Helper.__args[key]

    class UUID:
        @staticmethod
        def generate() -> str:
            import uuid
            return str(uuid.uuid4())

    class FS:
        @staticmethod
        def mkdir_if_not_exists(path):
            if not os.path.exists(path):
                os.makedirs(path)

        @staticmethod
        def is_exists(path, force: bool=False):
            if not os.path.exists(path):
                if force:
                    print(f"Path {path} does not exist")
                    fail()
                return False
            return True

        @staticmethod
        def is_file(path, force: bool=False):
            if not os.path.isfile(path):
                if force:
                    print(f"Path {path} is not a file")
                    fail()
                return False
            return True

        @staticmethod
        def is_dir(path, force: bool=False):
            if not os.path.isdir(path):
                if force:
                    print(f"Path {path} is not a directory")
                    fail()
                return False
            return True



def execute(main: Callable[[], None]):
    __parse_args()
    main()
    print(json.dumps(Flow.export_vars()))

def __parse_args():
    if sys.argv[1] == "":
        return
    input_args = json.loads(sys.argv[1])
    if "FlowArgs" in input_args:
        Flow.init_variables(input_args["FlowArgs"])
    if "HelperArgs" in input_args:
        __split_args(input_args["HelperArgs"])

def __split_args(helper_args: str):
    helper_args = helper_args.strip()
    if helper_args == "":
        return
    # [KEY1=VALUE1] [KEY2=VALUE2]
    args = {}
    for i in range(0, len(helper_args)):
        if helper_args[i] == "=":
            key, value = __find_kv(helper_args, i)
            args[key] = value
    Helper.init_args(args)
    print(f"Helper arguments: {args}")

def __find_kv(helper_args: str, equal_sign_index: int) -> [str, str]:
    front_str: str = helper_args[:equal_sign_index]
    last_left_bracket = front_str.rfind("[")
    if last_left_bracket == -1:
        raise ValueError("Invalid argument format")
    key: str = front_str[last_left_bracket + 1:]

    back_str: str = helper_args[equal_sign_index + 1:]
    next_left_bracket = back_str.find("[")
    if next_left_bracket != -1:
        back_str = back_str[:next_left_bracket]
    last_right_bracket = back_str.rfind("]")
    if last_right_bracket == -1:
        raise ValueError("Invalid argument format")
    value: str = back_str[:last_right_bracket]
    return key, value