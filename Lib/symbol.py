#! /usr/bin/env python

"""Non-terminal symbols of Python grammar (from "graminit.h")."""

#  This file is automatically generated; please don't muck it up!
#
#  To update the symbols in this file, 'cd' to the top directory of
#  the python source tree after building the interpreter and run:
#
#    python Lib/symbol.py

#--start constants--
single_input = 256
file_input = 257
eval_input = 258
decorator = 259
decorators = 260
funcdef = 261
parameters = 262
typedargslist = 263
tname = 264
tfpdef = 265
tfplist = 266
varargslist = 267
vname = 268
vfpdef = 269
vfplist = 270
stmt = 271
simple_stmt = 272
small_stmt = 273
expr_stmt = 274
augassign = 275
del_stmt = 276
pass_stmt = 277
flow_stmt = 278
break_stmt = 279
continue_stmt = 280
return_stmt = 281
yield_stmt = 282
raise_stmt = 283
import_stmt = 284
import_name = 285
import_from = 286
import_as_name = 287
dotted_as_name = 288
import_as_names = 289
dotted_as_names = 290
dotted_name = 291
global_stmt = 292
assert_stmt = 293
compound_stmt = 294
if_stmt = 295
while_stmt = 296
for_stmt = 297
try_stmt = 298
with_stmt = 299
with_var = 300
except_clause = 301
suite = 302
testlist_safe = 303
old_test = 304
old_lambdef = 305
test = 306
or_test = 307
and_test = 308
not_test = 309
comparison = 310
comp_op = 311
expr = 312
xor_expr = 313
and_expr = 314
shift_expr = 315
arith_expr = 316
term = 317
factor = 318
power = 319
atom = 320
listmaker = 321
testlist_gexp = 322
lambdef = 323
trailer = 324
subscriptlist = 325
subscript = 326
sliceop = 327
exprlist = 328
testlist = 329
dictsetmaker = 330
classdef = 331
arglist = 332
argument = 333
list_iter = 334
list_for = 335
list_if = 336
gen_iter = 337
gen_for = 338
gen_if = 339
testlist1 = 340
encoding_decl = 341
yield_expr = 342
#--end constants--

sym_name = {}
for _name, _value in list(globals().items()):
    if type(_value) is type(0):
        sym_name[_value] = _name


def main():
    import sys
    import token
    if len(sys.argv) == 1:
        sys.argv = sys.argv + ["Include/graminit.h", "Lib/symbol.py"]
    token.main()

if __name__ == "__main__":
    main()
