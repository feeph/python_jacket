#!/usr/bin/env python3
#
# testcases for typical cfg_cli usage
# (does not include 'expect-to-fail' tests)
#
# order is always the same
#  1)  initialize config options       <obj1> = cfgopts.ConfigOptions()
#  2)  register config option          <obj1>.register_cfgoption(...);
#  3)  initialize config parser        <obj2> = cfg_cli.CliParser(<obj1>, ...)
#  4a) define environment variables    <obj>.define_environment_variable(...)
#  4b) define commandline arguments    <obj>.define_*_argument(...)
#  5)  parse configuration             config = <obj2>.parse_and_verify(os.environ, sys.argv)
#  not shown:
#  6)  use configuration               main.do_something(**config)

import cfgopts
import cfg_cli


class Test:

    def setup_method(self, test_method):
        self.cfg_opts = cfgopts.ConfigOptions()
        self.sut = cfg_cli.CliParser(self.cfg_opts, "system under test")


    def test_positional_arguments(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument");
        self.cfg_opts.register_cfgoption(cfgoption="arg2", description="2nd argument");
        # order of execution defines order of arguments
        self.sut.define_positional_argument(cfgoption="arg1")
        self.sut.define_positional_argument(cfgoption="arg2")

        arguments = "program value1 value2".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config is not None
        assert config["arg1"] == "value1"
        assert config["arg2"] == "value2"


    def test_flag(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument");
        self.cfg_opts.register_cfgoption(cfgoption="arg2", description="2nd argument");
        self.cfg_opts.register_cfgoption(cfgoption="arg3", description="3nd argument");
        self.sut.define_flag_argument(cfgoption="arg1", long_name="--force")
        self.sut.define_flag_argument(cfgoption="arg2", long_name="--quiet", short_name="-q")
        self.sut.define_flag_argument(cfgoption="arg3", long_name="--dummy")

        arguments = "program --force -q".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config["arg1"] == 1
        assert config["arg2"] == 1
        assert config["arg3"] == 0  # wasn't set, defaults to 0


    def test_repeatable_flag(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument");
        self.sut.define_flag_argument(cfgoption="arg1", long_name="--verbose", short_name="-v", repeatable=True)

        arguments = "program -v -v".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config["arg1"] == 2  # number of occurrences


    # cfg_cli does not support bundled flags, e.g. "-vvv" (3x '-v')


    def test_named_arguments(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument");
        self.cfg_opts.register_cfgoption(cfgoption="arg2", description="2nd argument");
        self.sut.define_named_argument(cfgoption="arg1", long_name="--a1")
        self.sut.define_named_argument(cfgoption="arg2", long_name="--a2", short_name="-2")

        arguments = "program --a1=value1 -2 value2".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config["arg1"] == "value1"
        assert config["arg2"] == "value2"


    def test_mixed_arguments(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument");
        self.cfg_opts.register_cfgoption(cfgoption="arg2", description="2nd argument");
        self.cfg_opts.register_cfgoption(cfgoption="arg3", description="3rd argument");
        self.sut.define_named_argument(cfgoption="arg1", long_name="--a1")
        self.sut.define_flag_argument(cfgoption="arg2", long_name="--quiet", short_name="-q")
        self.sut.define_positional_argument(cfgoption="arg3")

        arguments = "program --a1=value1 -q value3".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config["arg1"] == "value1"
        assert config["arg2"] == 1
        assert config["arg3"] == "value3"


    def test_optional_arguments(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument", is_optional=True);
        self.cfg_opts.register_cfgoption(cfgoption="arg2", description="2nd argument");
        self.cfg_opts.register_cfgoption(cfgoption="arg3", description="3rd argument", is_optional=True);
        self.sut.define_named_argument(cfgoption="arg1", long_name="--a1")
        self.sut.define_positional_argument(cfgoption="arg2")
        self.sut.define_positional_argument(cfgoption="arg3")

        arguments = "program value2".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config["arg2"] == "value2"


    def test_verified_arguments(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument", pattern="(abc|def)", is_optional=True);
        self.cfg_opts.register_cfgoption(cfgoption="arg2", description="2nd argument", pattern="(abc|def)", is_optional=True);
        self.cfg_opts.register_cfgoption(cfgoption="arg3", description="3st argument", pattern="(ghi|jkl)", is_optional=True);
        self.cfg_opts.register_cfgoption(cfgoption="arg4", description="4th argument", pattern="(ghi|jkl)", is_optional=True);
        self.sut.define_named_argument(cfgoption="arg1", long_name="--a1")
        self.sut.define_named_argument(cfgoption="arg2", long_name="--a2")
        self.sut.define_positional_argument(cfgoption="arg3")
        self.sut.define_positional_argument(cfgoption="arg4")

        arguments = "program --a1=abc --a2=DEF ghi JKL".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config["arg1"] == "abc"
        assert "arg2" not in config     # argument was invalid
        assert config["arg3"] == "ghi"
        assert "arg4" not in config     # argument was invalid


    def test_default_value(self):
        self.cfg_opts.register_cfgoption(cfgoption="arg1", description="1st argument", default="abc", is_optional=True);
        self.sut.define_positional_argument(cfgoption="arg1")

        arguments = "program".split()
        config = self.sut.parse_and_verify({}, arguments)

        assert config["arg1"] == "abc"  # use default value
