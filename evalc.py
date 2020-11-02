#Changed by https://github.com/AstonishingBoy
"""Evaluate C++ code"""
# Author: @dzhingme_vangchuk

import logging
import os
import subprocess
from .. import loader, utils
logger = logging.getLogger(__name__)


@loader.tds
class CevalMod(loader.Module):
	"""тут был украинец/Слава Україні!"""
    """Выполнения C++ кода"""
    strings = {"name": "Ceval",
               "success": "Success!",
               "result": "**Evaluating :**\n\
```{prog}```\n**Compiler output :**\n\
```{compilation}```\n**Result :**\n```{result}```"}

    async def evalccmd(self, message):
        """Выполнения C++ кода"""
        prog = utils.get_args_raw(message)
        compile_cmd = 'g++ a.cpp'
        exec_cmd = "./a.out"
        with open("a.cpp", "w") as src:
            src.write(prog)
        compilation = subprocess.getoutput(compile_cmd)
        if not compilation:
            compilation = self.strings("success", message)
        result = subprocess.getoutput(exec_cmd)
        os.system("rm a.out && rm a.c")
        await message.edit(
            self.strings("result", message).format(
                prog=prog,
                compilation=compilation,
                result=result),
            parse_mode="Markdown")
