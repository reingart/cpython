# Non-terminal symbols of Python grammar (from "graminit.h")

single_input = 256
file_input = 257
eval_input = 258
funcdef = 259
parameters = 260
varargslist = 261
fpdef = 262
fplist = 263
stmt = 264
simple_stmt = 265
small_stmt = 266
expr_stmt = 267
print_stmt = 268
del_stmt = 269
pass_stmt = 270
flow_stmt = 271
break_stmt = 272
continue_stmt = 273
return_stmt = 274
raise_stmt = 275
import_stmt = 276
global_stmt = 277
access_stmt = 278
accesstype = 279
exec_stmt = 280
compound_stmt = 281
if_stmt = 282
while_stmt = 283
for_stmt = 284
try_stmt = 285
except_clause = 286
suite = 287
test = 288
and_test = 289
not_test = 290
comparison = 291
comp_op = 292
expr = 293
xor_expr = 294
and_expr = 295
shift_expr = 296
arith_expr = 297
term = 298
factor = 299
atom = 300
lambdef = 301
trailer = 302
subscript = 303
exprlist = 304
testlist = 305
dictmaker = 306
classdef = 307

names = dir()
sym_name = {}
for name in names:
	number = eval(name)
	sym_name[number] = name
