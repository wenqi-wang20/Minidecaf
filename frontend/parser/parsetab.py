
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programAnd Assign BitAnd BitNot BitOr Break Colon Continue Div Do Else Equal For Greater GreaterEqual Identifier If Int Integer LBrace LParen Less LessEqual Minus Mod Mul Not NotEqual Or Plus Question RBrace RParen Return Semi While Xor\n    empty :\n    \n    program : function\n    \n    type : Int\n    \n    function : type Identifier LParen RParen LBrace block RBrace\n    \n    block : block block_item\n    \n    block : empty\n    \n    block_item : statement\n        | declaration Semi\n    \n    statement : statement_matched\n        | statement_unmatched\n    \n    statement_matched : If LParen expression RParen statement_matched Else statement_matched\n    statement_unmatched : If LParen expression RParen statement_matched Else statement_unmatched\n    \n    statement_unmatched : If LParen expression RParen statement\n    \n    statement_matched : While LParen expression RParen statement_matched\n    statement_unmatched : While LParen expression RParen statement_unmatched\n    \n    statement_matched : Return expression Semi\n    \n    statement_matched : opt_expression Semi\n    \n    statement_matched : LBrace block RBrace\n    \n    statement_matched : Break Semi\n    \n    opt_expression : expression\n    \n    opt_expression : empty\n    \n    declaration : type Identifier\n    \n    declaration : type Identifier Assign expression\n    \n    expression : assignment\n    assignment : conditional\n    conditional : logical_or\n    logical_or : logical_and\n    logical_and : bit_or\n    bit_or : xor\n    xor : bit_and\n    bit_and : equality\n    equality : relational\n    relational : additive\n    additive : multiplicative\n    multiplicative : unary\n    unary : postfix\n    postfix : primary\n    \n    unary : Minus unary\n        | BitNot unary\n        | Not unary\n    \n    assignment : Identifier Assign expression\n    logical_or : logical_or Or logical_and\n    logical_and : logical_and And bit_or\n    bit_or : bit_or BitOr xor\n    xor : xor Xor bit_and\n    bit_and : bit_and BitAnd equality\n    equality : equality NotEqual relational\n        | equality Equal relational\n    relational : relational Less additive\n        | relational Greater additive\n        | relational LessEqual additive\n        | relational GreaterEqual additive\n    additive : additive Plus multiplicative\n        | additive Minus multiplicative\n    multiplicative : multiplicative Mul unary\n        | multiplicative Div unary\n        | multiplicative Mod unary\n    \n    conditional : logical_or Question expression Colon conditional\n    \n    primary : Integer\n    \n    primary : Identifier\n    \n    primary : LParen expression RParen\n    \n    statement_matched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_matched\n    statement_unmatched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_unmatched\n    statement_matched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_matched\n    statement_unmatched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_unmatched\n    \n    statement_matched : Do statement_matched While LParen expression RParen Semi\n    statement_unmatched : Do statement_unmatched While LParen expression RParen Semi\n    \n    statement_matched : Continue Semi\n    '
    
_lr_action_items = {'Int':([0,8,9,10,14,16,17,19,20,52,53,57,58,59,62,87,90,120,121,122,123,134,135,138,139,142,143,144,145,],[4,-1,4,-6,-1,-5,-7,-9,-10,4,-8,-17,-19,4,-68,-18,-16,-9,-13,-14,-15,-11,-12,-66,-67,-62,-63,-64,-65,]),'$end':([1,2,15,],[0,-2,-4,]),'Identifier':([3,4,8,9,10,11,13,14,16,17,19,20,24,28,42,45,46,50,52,53,54,55,57,58,59,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,87,90,113,114,115,116,117,118,119,120,121,122,123,129,130,131,134,135,138,139,140,141,142,143,144,145,],[5,-3,-1,12,-6,49,12,-1,-5,-7,-9,-10,12,12,81,81,81,12,12,-8,12,12,-17,-19,12,-68,12,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,12,-18,-16,12,12,12,12,12,12,81,-9,-13,-14,-15,12,12,12,-11,-12,-66,-67,12,12,-62,-63,-64,-65,]),'LParen':([5,8,9,10,13,14,16,17,19,20,22,23,24,27,28,42,45,46,50,52,53,54,55,57,58,59,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,87,90,93,94,113,114,115,116,117,118,119,120,121,122,123,129,130,131,134,135,138,139,140,141,142,143,144,145,],[6,-1,13,-6,13,-1,-5,-7,-9,-10,54,55,13,59,13,13,13,13,13,13,-8,13,13,-17,-19,13,-68,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,-18,-16,117,118,13,13,13,13,13,13,13,-9,-13,-14,-15,13,13,13,-11,-12,-66,-67,13,13,-62,-63,-64,-65,]),'RParen':([6,12,21,30,31,32,33,34,35,36,37,38,39,40,41,43,44,47,48,51,80,81,82,83,85,86,88,89,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,126,127,128,130,131,136,137,],[7,-60,-20,-21,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-59,86,-38,-60,-39,-40,-41,-61,113,114,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,132,133,-58,-1,-1,140,141,]),'LBrace':([7,8,9,10,14,16,17,19,20,28,52,53,57,58,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[8,-1,14,-6,-1,-5,-7,-9,-10,14,14,-8,-17,-19,-68,-18,-16,14,14,-9,-13,-14,-15,14,-11,-12,-66,-67,14,14,-62,-63,-64,-65,]),'RBrace':([8,9,10,14,16,17,19,20,52,53,57,58,62,87,90,120,121,122,123,134,135,138,139,142,143,144,145,],[-1,15,-6,-1,-5,-7,-9,-10,87,-8,-17,-19,-68,-18,-16,-9,-13,-14,-15,-11,-12,-66,-67,-62,-63,-64,-65,]),'If':([8,9,10,14,16,17,19,20,28,52,53,57,58,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[-1,22,-6,-1,-5,-7,-9,-10,22,22,-8,-17,-19,-68,-18,-16,22,22,-9,-13,-14,-15,22,-11,-12,-66,-67,22,22,-62,-63,-64,-65,]),'While':([8,9,10,14,16,17,19,20,28,52,53,57,58,60,61,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[-1,23,-6,-1,-5,-7,-9,-10,23,23,-8,-17,-19,93,94,-68,-18,-16,23,23,-9,-13,-14,-15,23,-11,-12,-66,-67,23,23,-62,-63,-64,-65,]),'Return':([8,9,10,14,16,17,19,20,28,52,53,57,58,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[-1,24,-6,-1,-5,-7,-9,-10,24,24,-8,-17,-19,-68,-18,-16,24,24,-9,-13,-14,-15,24,-11,-12,-66,-67,24,24,-62,-63,-64,-65,]),'Break':([8,9,10,14,16,17,19,20,28,52,53,57,58,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[-1,26,-6,-1,-5,-7,-9,-10,26,26,-8,-17,-19,-68,-18,-16,26,26,-9,-13,-14,-15,26,-11,-12,-66,-67,26,26,-62,-63,-64,-65,]),'For':([8,9,10,14,16,17,19,20,28,52,53,57,58,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[-1,27,-6,-1,-5,-7,-9,-10,27,27,-8,-17,-19,-68,-18,-16,27,27,-9,-13,-14,-15,27,-11,-12,-66,-67,27,27,-62,-63,-64,-65,]),'Do':([8,9,10,14,16,17,19,20,28,52,53,57,58,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[-1,28,-6,-1,-5,-7,-9,-10,28,28,-8,-17,-19,-68,-18,-16,28,28,-9,-13,-14,-15,28,-11,-12,-66,-67,28,28,-62,-63,-64,-65,]),'Continue':([8,9,10,14,16,17,19,20,28,52,53,57,58,62,87,90,113,114,120,121,122,123,129,134,135,138,139,140,141,142,143,144,145,],[-1,29,-6,-1,-5,-7,-9,-10,29,29,-8,-17,-19,-68,-18,-16,29,29,-9,-13,-14,-15,29,-11,-12,-66,-67,29,29,-62,-63,-64,-65,]),'Minus':([8,9,10,12,13,14,16,17,19,20,24,28,40,41,42,43,44,45,46,47,48,50,52,53,54,55,57,58,59,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,90,103,104,105,106,107,108,109,110,111,113,114,115,116,117,118,119,120,121,122,123,129,130,131,134,135,138,139,140,141,142,143,144,145,],[-1,42,-6,-60,42,-1,-5,-7,-9,-10,42,42,76,-34,42,-35,-36,42,42,-37,-59,42,42,-8,42,42,-17,-19,42,-68,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,-38,-60,-39,-40,42,-61,-18,-16,76,76,76,76,-53,-54,-55,-56,-57,42,42,42,42,42,42,42,-9,-13,-14,-15,42,42,42,-11,-12,-66,-67,42,42,-62,-63,-64,-65,]),'BitNot':([8,9,10,13,14,16,17,19,20,24,28,42,45,46,50,52,53,54,55,57,58,59,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,87,90,113,114,115,116,117,118,119,120,121,122,123,129,130,131,134,135,138,139,140,141,142,143,144,145,],[-1,45,-6,45,-1,-5,-7,-9,-10,45,45,45,45,45,45,45,-8,45,45,-17,-19,45,-68,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,-18,-16,45,45,45,45,45,45,45,-9,-13,-14,-15,45,45,45,-11,-12,-66,-67,45,45,-62,-63,-64,-65,]),'Not':([8,9,10,13,14,16,17,19,20,24,28,42,45,46,50,52,53,54,55,57,58,59,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,87,90,113,114,115,116,117,118,119,120,121,122,123,129,130,131,134,135,138,139,140,141,142,143,144,145,],[-1,46,-6,46,-1,-5,-7,-9,-10,46,46,46,46,46,46,46,-8,46,46,-17,-19,46,-68,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,-18,-16,46,46,46,46,46,46,46,-9,-13,-14,-15,46,46,46,-11,-12,-66,-67,46,46,-62,-63,-64,-65,]),'Integer':([8,9,10,13,14,16,17,19,20,24,28,42,45,46,50,52,53,54,55,57,58,59,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,87,90,113,114,115,116,117,118,119,120,121,122,123,129,130,131,134,135,138,139,140,141,142,143,144,145,],[-1,48,-6,48,-1,-5,-7,-9,-10,48,48,48,48,48,48,48,-8,48,48,-17,-19,48,-68,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,-18,-16,48,48,48,48,48,48,48,-9,-13,-14,-15,48,48,48,-11,-12,-66,-67,48,48,-62,-63,-64,-65,]),'Semi':([8,9,10,12,14,16,17,18,19,20,21,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,43,44,47,48,49,52,53,56,57,58,59,62,80,81,82,83,85,86,87,90,91,92,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,120,121,122,123,124,125,128,129,132,133,134,135,138,139,140,141,142,143,144,145,],[-1,-1,-6,-60,-1,-5,-7,53,-9,-10,-20,57,58,-1,62,-21,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-59,-22,-1,-8,90,-17,-19,-1,-68,-38,-60,-39,-40,-41,-61,-18,-16,115,116,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-23,-1,-1,-1,-1,-9,-13,-14,-15,130,131,-58,-1,138,139,-11,-12,-66,-67,-1,-1,-62,-63,-64,-65,]),'Assign':([12,49,],[50,84,]),'Mul':([12,41,43,44,47,48,80,81,82,83,86,107,108,109,110,111,],[-60,77,-35,-36,-37,-59,-38,-60,-39,-40,-61,77,77,-55,-56,-57,]),'Div':([12,41,43,44,47,48,80,81,82,83,86,107,108,109,110,111,],[-60,78,-35,-36,-37,-59,-38,-60,-39,-40,-61,78,78,-55,-56,-57,]),'Mod':([12,41,43,44,47,48,80,81,82,83,86,107,108,109,110,111,],[-60,79,-35,-36,-37,-59,-38,-60,-39,-40,-61,79,79,-55,-56,-57,]),'Plus':([12,40,41,43,44,47,48,80,81,82,83,86,103,104,105,106,107,108,109,110,111,],[-60,75,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,75,75,75,75,-53,-54,-55,-56,-57,]),'Less':([12,39,40,41,43,44,47,48,80,81,82,83,86,101,102,103,104,105,106,107,108,109,110,111,],[-60,71,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,71,71,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'Greater':([12,39,40,41,43,44,47,48,80,81,82,83,86,101,102,103,104,105,106,107,108,109,110,111,],[-60,72,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,72,72,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'LessEqual':([12,39,40,41,43,44,47,48,80,81,82,83,86,101,102,103,104,105,106,107,108,109,110,111,],[-60,73,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,73,73,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'GreaterEqual':([12,39,40,41,43,44,47,48,80,81,82,83,86,101,102,103,104,105,106,107,108,109,110,111,],[-60,74,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,74,74,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'NotEqual':([12,38,39,40,41,43,44,47,48,80,81,82,83,86,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,69,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,69,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'Equal':([12,38,39,40,41,43,44,47,48,80,81,82,83,86,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,70,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,70,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'BitAnd':([12,37,38,39,40,41,43,44,47,48,80,81,82,83,86,99,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,68,-31,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,68,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'Xor':([12,36,37,38,39,40,41,43,44,47,48,80,81,82,83,86,98,99,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,67,-30,-31,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,67,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'BitOr':([12,35,36,37,38,39,40,41,43,44,47,48,80,81,82,83,86,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,66,-29,-30,-31,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,66,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'And':([12,34,35,36,37,38,39,40,41,43,44,47,48,80,81,82,83,86,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,65,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,65,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'Question':([12,33,34,35,36,37,38,39,40,41,43,44,47,48,80,81,82,83,86,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,63,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'Or':([12,33,34,35,36,37,38,39,40,41,43,44,47,48,80,81,82,83,86,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,],[-60,64,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-61,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,]),'Colon':([12,31,32,33,34,35,36,37,38,39,40,41,43,44,47,48,80,81,82,83,85,86,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,128,],[-60,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-59,-38,-60,-39,-40,-41,-61,119,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,]),'Else':([57,58,62,87,90,120,122,134,138,142,144,],[-17,-19,-68,-18,-16,129,-14,-11,-66,-62,-64,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'function':([0,],[2,]),'type':([0,9,52,59,],[3,11,11,11,]),'block':([8,14,],[9,52,]),'empty':([8,9,14,28,52,59,113,114,115,116,129,130,131,140,141,],[10,30,10,30,30,30,30,30,30,30,30,30,30,30,30,]),'block_item':([9,52,],[16,16,]),'statement':([9,52,113,],[17,17,121,]),'declaration':([9,52,59,],[18,18,92,]),'statement_matched':([9,28,52,113,114,129,140,141,],[19,60,19,120,122,134,142,144,]),'statement_unmatched':([9,28,52,113,114,129,140,141,],[20,61,20,20,123,135,143,145,]),'expression':([9,13,24,28,50,52,54,55,59,63,84,113,114,115,116,117,118,129,130,131,140,141,],[21,51,56,21,85,21,88,89,21,95,112,21,21,21,21,126,127,21,21,21,21,21,]),'opt_expression':([9,28,52,59,113,114,115,116,129,130,131,140,141,],[25,25,25,91,25,25,124,125,25,136,137,25,25,]),'assignment':([9,13,24,28,50,52,54,55,59,63,84,113,114,115,116,117,118,129,130,131,140,141,],[31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'conditional':([9,13,24,28,50,52,54,55,59,63,84,113,114,115,116,117,118,119,129,130,131,140,141,],[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,128,32,32,32,32,32,]),'logical_or':([9,13,24,28,50,52,54,55,59,63,84,113,114,115,116,117,118,119,129,130,131,140,141,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'logical_and':([9,13,24,28,50,52,54,55,59,63,64,84,113,114,115,116,117,118,119,129,130,131,140,141,],[34,34,34,34,34,34,34,34,34,34,96,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'bit_or':([9,13,24,28,50,52,54,55,59,63,64,65,84,113,114,115,116,117,118,119,129,130,131,140,141,],[35,35,35,35,35,35,35,35,35,35,35,97,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'xor':([9,13,24,28,50,52,54,55,59,63,64,65,66,84,113,114,115,116,117,118,119,129,130,131,140,141,],[36,36,36,36,36,36,36,36,36,36,36,36,98,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'bit_and':([9,13,24,28,50,52,54,55,59,63,64,65,66,67,84,113,114,115,116,117,118,119,129,130,131,140,141,],[37,37,37,37,37,37,37,37,37,37,37,37,37,99,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'equality':([9,13,24,28,50,52,54,55,59,63,64,65,66,67,68,84,113,114,115,116,117,118,119,129,130,131,140,141,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,100,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'relational':([9,13,24,28,50,52,54,55,59,63,64,65,66,67,68,69,70,84,113,114,115,116,117,118,119,129,130,131,140,141,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,101,102,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'additive':([9,13,24,28,50,52,54,55,59,63,64,65,66,67,68,69,70,71,72,73,74,84,113,114,115,116,117,118,119,129,130,131,140,141,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,103,104,105,106,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'multiplicative':([9,13,24,28,50,52,54,55,59,63,64,65,66,67,68,69,70,71,72,73,74,75,76,84,113,114,115,116,117,118,119,129,130,131,140,141,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,107,108,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'unary':([9,13,24,28,42,45,46,50,52,54,55,59,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,113,114,115,116,117,118,119,129,130,131,140,141,],[43,43,43,43,80,82,83,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,109,110,111,43,43,43,43,43,43,43,43,43,43,43,43,43,]),'postfix':([9,13,24,28,42,45,46,50,52,54,55,59,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,113,114,115,116,117,118,119,129,130,131,140,141,],[44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,]),'primary':([9,13,24,28,42,45,46,50,52,54,55,59,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,84,113,114,115,116,117,118,119,129,130,131,140,141,],[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('empty -> <empty>','empty',0,'p_empty','ply_parser.py',38),
  ('program -> function','program',1,'p_program','ply_parser.py',45),
  ('type -> Int','type',1,'p_type','ply_parser.py',52),
  ('function -> type Identifier LParen RParen LBrace block RBrace','function',7,'p_function_def','ply_parser.py',59),
  ('block -> block block_item','block',2,'p_block','ply_parser.py',66),
  ('block -> empty','block',1,'p_block_empty','ply_parser.py',75),
  ('block_item -> statement','block_item',1,'p_block_item','ply_parser.py',82),
  ('block_item -> declaration Semi','block_item',2,'p_block_item','ply_parser.py',83),
  ('statement -> statement_matched','statement',1,'p_statement','ply_parser.py',90),
  ('statement -> statement_unmatched','statement',1,'p_statement','ply_parser.py',91),
  ('statement_matched -> If LParen expression RParen statement_matched Else statement_matched','statement_matched',7,'p_if_else','ply_parser.py',98),
  ('statement_unmatched -> If LParen expression RParen statement_matched Else statement_unmatched','statement_unmatched',7,'p_if_else','ply_parser.py',99),
  ('statement_unmatched -> If LParen expression RParen statement','statement_unmatched',5,'p_if','ply_parser.py',106),
  ('statement_matched -> While LParen expression RParen statement_matched','statement_matched',5,'p_while','ply_parser.py',113),
  ('statement_unmatched -> While LParen expression RParen statement_unmatched','statement_unmatched',5,'p_while','ply_parser.py',114),
  ('statement_matched -> Return expression Semi','statement_matched',3,'p_return','ply_parser.py',121),
  ('statement_matched -> opt_expression Semi','statement_matched',2,'p_expression_statement','ply_parser.py',128),
  ('statement_matched -> LBrace block RBrace','statement_matched',3,'p_block_statement','ply_parser.py',135),
  ('statement_matched -> Break Semi','statement_matched',2,'p_break','ply_parser.py',142),
  ('opt_expression -> expression','opt_expression',1,'p_opt_expression','ply_parser.py',149),
  ('opt_expression -> empty','opt_expression',1,'p_opt_expression_empty','ply_parser.py',156),
  ('declaration -> type Identifier','declaration',2,'p_declaration','ply_parser.py',163),
  ('declaration -> type Identifier Assign expression','declaration',4,'p_declaration_init','ply_parser.py',170),
  ('expression -> assignment','expression',1,'p_expression_precedence','ply_parser.py',177),
  ('assignment -> conditional','assignment',1,'p_expression_precedence','ply_parser.py',178),
  ('conditional -> logical_or','conditional',1,'p_expression_precedence','ply_parser.py',179),
  ('logical_or -> logical_and','logical_or',1,'p_expression_precedence','ply_parser.py',180),
  ('logical_and -> bit_or','logical_and',1,'p_expression_precedence','ply_parser.py',181),
  ('bit_or -> xor','bit_or',1,'p_expression_precedence','ply_parser.py',182),
  ('xor -> bit_and','xor',1,'p_expression_precedence','ply_parser.py',183),
  ('bit_and -> equality','bit_and',1,'p_expression_precedence','ply_parser.py',184),
  ('equality -> relational','equality',1,'p_expression_precedence','ply_parser.py',185),
  ('relational -> additive','relational',1,'p_expression_precedence','ply_parser.py',186),
  ('additive -> multiplicative','additive',1,'p_expression_precedence','ply_parser.py',187),
  ('multiplicative -> unary','multiplicative',1,'p_expression_precedence','ply_parser.py',188),
  ('unary -> postfix','unary',1,'p_expression_precedence','ply_parser.py',189),
  ('postfix -> primary','postfix',1,'p_expression_precedence','ply_parser.py',190),
  ('unary -> Minus unary','unary',2,'p_unary_expression','ply_parser.py',197),
  ('unary -> BitNot unary','unary',2,'p_unary_expression','ply_parser.py',198),
  ('unary -> Not unary','unary',2,'p_unary_expression','ply_parser.py',199),
  ('assignment -> Identifier Assign expression','assignment',3,'p_binary_expression','ply_parser.py',206),
  ('logical_or -> logical_or Or logical_and','logical_or',3,'p_binary_expression','ply_parser.py',207),
  ('logical_and -> logical_and And bit_or','logical_and',3,'p_binary_expression','ply_parser.py',208),
  ('bit_or -> bit_or BitOr xor','bit_or',3,'p_binary_expression','ply_parser.py',209),
  ('xor -> xor Xor bit_and','xor',3,'p_binary_expression','ply_parser.py',210),
  ('bit_and -> bit_and BitAnd equality','bit_and',3,'p_binary_expression','ply_parser.py',211),
  ('equality -> equality NotEqual relational','equality',3,'p_binary_expression','ply_parser.py',212),
  ('equality -> equality Equal relational','equality',3,'p_binary_expression','ply_parser.py',213),
  ('relational -> relational Less additive','relational',3,'p_binary_expression','ply_parser.py',214),
  ('relational -> relational Greater additive','relational',3,'p_binary_expression','ply_parser.py',215),
  ('relational -> relational LessEqual additive','relational',3,'p_binary_expression','ply_parser.py',216),
  ('relational -> relational GreaterEqual additive','relational',3,'p_binary_expression','ply_parser.py',217),
  ('additive -> additive Plus multiplicative','additive',3,'p_binary_expression','ply_parser.py',218),
  ('additive -> additive Minus multiplicative','additive',3,'p_binary_expression','ply_parser.py',219),
  ('multiplicative -> multiplicative Mul unary','multiplicative',3,'p_binary_expression','ply_parser.py',220),
  ('multiplicative -> multiplicative Div unary','multiplicative',3,'p_binary_expression','ply_parser.py',221),
  ('multiplicative -> multiplicative Mod unary','multiplicative',3,'p_binary_expression','ply_parser.py',222),
  ('conditional -> logical_or Question expression Colon conditional','conditional',5,'p_conditional_expression','ply_parser.py',229),
  ('primary -> Integer','primary',1,'p_int_literal_expression','ply_parser.py',236),
  ('primary -> Identifier','primary',1,'p_identifier_expression','ply_parser.py',243),
  ('primary -> LParen expression RParen','primary',3,'p_brace_expression','ply_parser.py',250),
  ('statement_matched -> For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_matched','statement_matched',9,'p_for','ply_parser.py',274),
  ('statement_unmatched -> For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_unmatched','statement_unmatched',9,'p_for','ply_parser.py',275),
  ('statement_matched -> For LParen declaration Semi opt_expression Semi opt_expression RParen statement_matched','statement_matched',9,'p_for','ply_parser.py',276),
  ('statement_unmatched -> For LParen declaration Semi opt_expression Semi opt_expression RParen statement_unmatched','statement_unmatched',9,'p_for','ply_parser.py',277),
  ('statement_matched -> Do statement_matched While LParen expression RParen Semi','statement_matched',7,'p_dowhile','ply_parser.py',284),
  ('statement_unmatched -> Do statement_unmatched While LParen expression RParen Semi','statement_unmatched',7,'p_dowhile','ply_parser.py',285),
  ('statement_matched -> Continue Semi','statement_matched',2,'p_continue','ply_parser.py',292),
]
