
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programAnd Assign BitAnd BitNot BitOr Break Colon Comma Continue Div Do Else Equal For Greater GreaterEqual Identifier If Int Integer LBrace LBracket LParen Less LessEqual Minus Mod Mul Not NotEqual Or Plus Question RBrace RBracket RParen Return Semi While Xor\n    empty :\n    \n    program : program function\n    \n    program : function\n    \n    program : program declaration Semi\n    \n    program : declaration Semi\n    \n    type : Int\n    \n    function : type Identifier LParen parameter_list RParen LBrace block RBrace\n    \n    function : type Identifier LParen parameter_list RParen Semi\n    \n    block : block block_item\n    \n    block : empty\n    \n    block_item : statement\n        | declaration Semi\n    \n    statement : statement_matched\n        | statement_unmatched\n    \n    statement_matched : If LParen expression RParen statement_matched Else statement_matched\n    statement_unmatched : If LParen expression RParen statement_matched Else statement_unmatched\n    \n    statement_unmatched : If LParen expression RParen statement\n    \n    statement_matched : While LParen expression RParen statement_matched\n    statement_unmatched : While LParen expression RParen statement_unmatched\n    \n    statement_matched : Return expression Semi\n    \n    statement_matched : opt_expression Semi\n    \n    statement_matched : LBrace block RBrace\n    \n    statement_matched : Break Semi\n    \n    opt_expression : expression\n    \n    opt_expression : empty\n    \n    declaration : type Identifier\n    \n    declaration : type Identifier Assign expression\n    \n    expression : assignment\n    assignment : conditional\n    conditional : logical_or\n    logical_or : logical_and\n    logical_and : bit_or\n    bit_or : xor\n    xor : bit_and\n    bit_and : equality\n    equality : relational\n    relational : additive\n    additive : multiplicative\n    multiplicative : unary\n    unary : postfix\n    postfix : primary\n    \n    unary : Minus unary\n        | BitNot unary\n        | Not unary\n    \n    assignment : Identifier Assign expression\n    logical_or : logical_or Or logical_and\n    logical_and : logical_and And bit_or\n    bit_or : bit_or BitOr xor\n    xor : xor Xor bit_and\n    bit_and : bit_and BitAnd equality\n    equality : equality NotEqual relational\n        | equality Equal relational\n    relational : relational Less additive\n        | relational Greater additive\n        | relational LessEqual additive\n        | relational GreaterEqual additive\n    additive : additive Plus multiplicative\n        | additive Minus multiplicative\n    multiplicative : multiplicative Mul unary\n        | multiplicative Div unary\n        | multiplicative Mod unary\n    \n    conditional : logical_or Question expression Colon conditional\n    \n    primary : Integer\n    \n    primary : Identifier\n    \n    primary : LParen expression RParen\n    \n    statement_matched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_matched\n    statement_unmatched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_unmatched\n    statement_matched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_matched\n    statement_unmatched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_unmatched\n    \n    statement_matched : Do statement_matched While LParen expression RParen Semi\n    statement_unmatched : Do statement_unmatched While LParen expression RParen Semi\n    \n    statement_matched : Continue Semi\n    \n    parameter_item : type Identifier\n    \n    parameter_list : parameter_list Comma parameter_item\n    \n    parameter_list : parameter_item\n    \n    parameter_list : empty\n    \n    expression_list : expression_list Comma expression\n    \n    expression_list : expression\n    \n    expression_list : empty\n    \n    postfix : Identifier LParen expression_list RParen\n    '
    
_lr_action_items = {'Int':([0,1,2,6,8,10,11,40,65,66,90,91,96,97,98,99,101,102,116,117,121,122,123,126,127,130,141,142,143,144,154,155,158,159,162,163,164,165,],[5,5,-3,-2,-5,-4,5,5,-1,-8,5,-10,-1,-7,-9,-11,-13,-14,5,-12,-21,-23,5,-72,-22,-20,-13,-17,-18,-19,-15,-16,-70,-71,-66,-67,-68,-69,]),'$end':([1,2,6,8,10,66,97,],[0,-3,-2,-5,-4,-8,-7,]),'Semi':([3,7,9,17,18,19,20,21,22,23,24,25,26,27,28,29,31,32,35,37,39,60,61,62,63,65,68,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,96,98,99,100,101,102,103,107,108,110,111,112,114,115,116,117,120,121,122,123,126,127,130,131,132,135,136,137,138,141,142,143,144,145,146,149,152,153,154,155,158,159,160,161,162,163,164,165,],[8,10,-26,-64,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,66,-42,-64,-43,-44,-1,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-1,-10,-80,-1,-9,-11,117,-13,-14,-24,121,122,-1,126,-25,-62,-26,-1,-12,130,-21,-23,-1,-72,-22,-20,137,138,-1,-1,-1,-1,-13,-17,-18,-19,150,151,-1,158,159,-15,-16,-70,-71,-1,-1,-66,-67,-68,-69,]),'Identifier':([4,5,12,13,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,65,90,91,93,94,95,96,98,99,101,102,106,110,116,117,118,119,121,122,123,126,127,130,135,136,137,138,139,140,141,142,143,144,149,150,151,154,155,158,159,160,161,162,163,164,165,],[9,-6,17,38,61,61,61,17,17,17,17,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,-1,17,-10,17,61,115,-1,-9,-11,-13,-14,17,17,17,-12,17,17,-21,-23,17,-72,-22,-20,17,17,17,17,17,17,-13,-17,-18,-19,17,17,17,-15,-16,-70,-71,17,17,-66,-67,-68,-69,]),'LParen':([9,12,17,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,61,65,90,91,93,94,96,98,99,101,102,104,105,106,109,110,116,117,118,119,121,122,123,126,127,130,133,134,135,136,137,138,139,140,141,142,143,144,149,150,151,154,155,158,159,160,161,162,163,164,165,],[11,36,42,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,42,-1,36,-10,36,36,-1,-9,-11,-13,-14,118,119,36,123,36,36,-12,36,36,-21,-23,36,-72,-22,-20,139,140,36,36,36,36,36,36,-13,-17,-18,-19,36,36,36,-15,-16,-70,-71,36,36,-66,-67,-68,-69,]),'Assign':([9,17,115,],[12,41,12,]),'RParen':([11,14,15,16,17,19,20,21,22,23,24,25,26,27,28,29,31,32,35,37,38,42,60,61,62,63,64,67,68,69,70,71,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,103,112,113,114,128,129,147,148,150,151,156,157,],[-1,39,-75,-76,-64,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,-73,-1,-42,-64,-43,-44,89,-74,-45,92,-78,-79,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,-24,-25,-77,-62,135,136,152,153,-1,-1,160,161,]),'Comma':([11,14,15,16,17,19,20,21,22,23,24,25,26,27,28,29,31,32,35,37,38,42,60,61,62,63,67,68,69,70,71,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,113,114,],[-1,40,-75,-76,-64,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,-73,-1,-42,-64,-43,-44,-74,-45,93,-78,-79,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,-77,-62,]),'Minus':([12,17,28,29,30,31,32,33,34,35,36,37,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,96,98,99,101,102,106,110,116,117,118,119,121,122,123,126,127,130,135,136,137,138,139,140,141,142,143,144,149,150,151,154,155,158,159,160,161,162,163,164,165,],[30,-64,56,-38,30,-39,-40,30,30,-41,30,-63,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,-42,-64,-43,-44,-1,56,56,56,56,-57,-58,-59,-60,-61,-65,30,-10,-80,30,30,-1,-9,-11,-13,-14,30,30,30,-12,30,30,-21,-23,30,-72,-22,-20,30,30,30,30,30,30,-13,-17,-18,-19,30,30,30,-15,-16,-70,-71,30,30,-66,-67,-68,-69,]),'BitNot':([12,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,65,90,91,93,94,96,98,99,101,102,106,110,116,117,118,119,121,122,123,126,127,130,135,136,137,138,139,140,141,142,143,144,149,150,151,154,155,158,159,160,161,162,163,164,165,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,-1,33,-10,33,33,-1,-9,-11,-13,-14,33,33,33,-12,33,33,-21,-23,33,-72,-22,-20,33,33,33,33,33,33,-13,-17,-18,-19,33,33,33,-15,-16,-70,-71,33,33,-66,-67,-68,-69,]),'Not':([12,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,65,90,91,93,94,96,98,99,101,102,106,110,116,117,118,119,121,122,123,126,127,130,135,136,137,138,139,140,141,142,143,144,149,150,151,154,155,158,159,160,161,162,163,164,165,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,-1,34,-10,34,34,-1,-9,-11,-13,-14,34,34,34,-12,34,34,-21,-23,34,-72,-22,-20,34,34,34,34,34,34,-13,-17,-18,-19,34,34,34,-15,-16,-70,-71,34,34,-66,-67,-68,-69,]),'Integer':([12,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,65,90,91,93,94,96,98,99,101,102,106,110,116,117,118,119,121,122,123,126,127,130,135,136,137,138,139,140,141,142,143,144,149,150,151,154,155,158,159,160,161,162,163,164,165,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,-1,37,-10,37,37,-1,-9,-11,-13,-14,37,37,37,-12,37,37,-21,-23,37,-72,-22,-20,37,37,37,37,37,37,-13,-17,-18,-19,37,37,37,-15,-16,-70,-71,37,37,-66,-67,-68,-69,]),'Mul':([17,29,31,32,35,37,60,61,62,63,84,85,86,87,88,89,92,],[-64,57,-39,-40,-41,-63,-42,-64,-43,-44,57,57,-59,-60,-61,-65,-80,]),'Div':([17,29,31,32,35,37,60,61,62,63,84,85,86,87,88,89,92,],[-64,58,-39,-40,-41,-63,-42,-64,-43,-44,58,58,-59,-60,-61,-65,-80,]),'Mod':([17,29,31,32,35,37,60,61,62,63,84,85,86,87,88,89,92,],[-64,59,-39,-40,-41,-63,-42,-64,-43,-44,59,59,-59,-60,-61,-65,-80,]),'Plus':([17,28,29,31,32,35,37,60,61,62,63,80,81,82,83,84,85,86,87,88,89,92,],[-64,55,-38,-39,-40,-41,-63,-42,-64,-43,-44,55,55,55,55,-57,-58,-59,-60,-61,-65,-80,]),'Less':([17,27,28,29,31,32,35,37,60,61,62,63,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,51,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,51,51,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'Greater':([17,27,28,29,31,32,35,37,60,61,62,63,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,52,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,52,52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'LessEqual':([17,27,28,29,31,32,35,37,60,61,62,63,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,53,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,53,53,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'GreaterEqual':([17,27,28,29,31,32,35,37,60,61,62,63,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,54,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,54,54,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'NotEqual':([17,26,27,28,29,31,32,35,37,60,61,62,63,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,49,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,49,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'Equal':([17,26,27,28,29,31,32,35,37,60,61,62,63,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,50,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'BitAnd':([17,25,26,27,28,29,31,32,35,37,60,61,62,63,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,48,-35,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,48,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'Xor':([17,24,25,26,27,28,29,31,32,35,37,60,61,62,63,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,47,-34,-35,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,47,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'BitOr':([17,23,24,25,26,27,28,29,31,32,35,37,60,61,62,63,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,46,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,46,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'And':([17,22,23,24,25,26,27,28,29,31,32,35,37,60,61,62,63,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,45,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,45,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'Question':([17,21,22,23,24,25,26,27,28,29,31,32,35,37,60,61,62,63,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,43,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'Or':([17,21,22,23,24,25,26,27,28,29,31,32,35,37,60,61,62,63,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,],[-64,44,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,]),'Colon':([17,19,20,21,22,23,24,25,26,27,28,29,31,32,35,37,60,61,62,63,68,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,92,114,],[-64,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,-41,-63,-42,-64,-43,-44,-45,94,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-65,-80,-62,]),'LBrace':([39,65,90,91,96,98,99,101,102,110,116,117,121,122,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[65,-1,96,-10,-1,-9,-11,-13,-14,96,96,-12,-21,-23,-72,-22,-20,96,96,-13,-17,-18,-19,96,-15,-16,-70,-71,96,96,-66,-67,-68,-69,]),'RBrace':([65,90,91,96,98,99,101,102,116,117,121,122,126,127,130,141,142,143,144,154,155,158,159,162,163,164,165,],[-1,97,-10,-1,-9,-11,-13,-14,127,-12,-21,-23,-72,-22,-20,-13,-17,-18,-19,-15,-16,-70,-71,-66,-67,-68,-69,]),'If':([65,90,91,96,98,99,101,102,110,116,117,121,122,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[-1,104,-10,-1,-9,-11,-13,-14,104,104,-12,-21,-23,-72,-22,-20,104,104,-13,-17,-18,-19,104,-15,-16,-70,-71,104,104,-66,-67,-68,-69,]),'While':([65,90,91,96,98,99,101,102,110,116,117,121,122,124,125,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[-1,105,-10,-1,-9,-11,-13,-14,105,105,-12,-21,-23,133,134,-72,-22,-20,105,105,-13,-17,-18,-19,105,-15,-16,-70,-71,105,105,-66,-67,-68,-69,]),'Return':([65,90,91,96,98,99,101,102,110,116,117,121,122,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[-1,106,-10,-1,-9,-11,-13,-14,106,106,-12,-21,-23,-72,-22,-20,106,106,-13,-17,-18,-19,106,-15,-16,-70,-71,106,106,-66,-67,-68,-69,]),'Break':([65,90,91,96,98,99,101,102,110,116,117,121,122,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[-1,108,-10,-1,-9,-11,-13,-14,108,108,-12,-21,-23,-72,-22,-20,108,108,-13,-17,-18,-19,108,-15,-16,-70,-71,108,108,-66,-67,-68,-69,]),'For':([65,90,91,96,98,99,101,102,110,116,117,121,122,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[-1,109,-10,-1,-9,-11,-13,-14,109,109,-12,-21,-23,-72,-22,-20,109,109,-13,-17,-18,-19,109,-15,-16,-70,-71,109,109,-66,-67,-68,-69,]),'Do':([65,90,91,96,98,99,101,102,110,116,117,121,122,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[-1,110,-10,-1,-9,-11,-13,-14,110,110,-12,-21,-23,-72,-22,-20,110,110,-13,-17,-18,-19,110,-15,-16,-70,-71,110,110,-66,-67,-68,-69,]),'Continue':([65,90,91,96,98,99,101,102,110,116,117,121,122,126,127,130,135,136,141,142,143,144,149,154,155,158,159,160,161,162,163,164,165,],[-1,111,-10,-1,-9,-11,-13,-14,111,111,-12,-21,-23,-72,-22,-20,111,111,-13,-17,-18,-19,111,-15,-16,-70,-71,111,111,-66,-67,-68,-69,]),'Else':([121,122,126,127,130,141,143,154,158,162,164,],[-21,-23,-72,-22,-20,149,-18,-15,-70,-66,-68,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'function':([0,1,],[2,6,]),'declaration':([0,1,90,116,123,],[3,7,100,100,132,]),'type':([0,1,11,40,90,116,123,],[4,4,13,13,95,95,95,]),'parameter_list':([11,],[14,]),'parameter_item':([11,40,],[15,67,]),'empty':([11,42,65,90,96,110,116,123,135,136,137,138,149,150,151,160,161,],[16,71,91,112,91,112,112,112,112,112,112,112,112,112,112,112,112,]),'expression':([12,36,41,42,43,90,93,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[18,64,68,70,72,103,113,120,103,103,128,129,103,103,103,103,103,147,148,103,103,103,103,103,]),'assignment':([12,36,41,42,43,90,93,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'conditional':([12,36,41,42,43,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[20,20,20,20,20,20,20,114,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,]),'logical_or':([12,36,41,42,43,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'logical_and':([12,36,41,42,43,44,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[22,22,22,22,22,73,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'bit_or':([12,36,41,42,43,44,45,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[23,23,23,23,23,23,74,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'xor':([12,36,41,42,43,44,45,46,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[24,24,24,24,24,24,24,75,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'bit_and':([12,36,41,42,43,44,45,46,47,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[25,25,25,25,25,25,25,25,76,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'equality':([12,36,41,42,43,44,45,46,47,48,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[26,26,26,26,26,26,26,26,26,77,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'relational':([12,36,41,42,43,44,45,46,47,48,49,50,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[27,27,27,27,27,27,27,27,27,27,78,79,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'additive':([12,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[28,28,28,28,28,28,28,28,28,28,28,28,80,81,82,83,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'multiplicative':([12,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,84,85,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,]),'unary':([12,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[31,60,62,63,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,86,87,88,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'postfix':([12,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,]),'primary':([12,30,33,34,36,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,90,93,94,106,110,116,118,119,123,135,136,137,138,139,140,149,150,151,160,161,],[35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'expression_list':([42,],[69,]),'block':([65,96,],[90,116,]),'block_item':([90,116,],[98,98,]),'statement':([90,116,135,],[99,99,142,]),'statement_matched':([90,110,116,135,136,149,160,161,],[101,124,101,141,143,154,162,164,]),'statement_unmatched':([90,110,116,135,136,149,160,161,],[102,125,102,102,144,155,163,165,]),'opt_expression':([90,110,116,123,135,136,137,138,149,150,151,160,161,],[107,107,107,131,107,107,145,146,107,156,157,107,107,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('empty -> <empty>','empty',0,'p_empty','ply_parser.py',38),
  ('program -> program function','program',2,'p_program','ply_parser.py',46),
  ('program -> function','program',1,'p_program_single_function','ply_parser.py',54),
  ('program -> program declaration Semi','program',3,'p_global_var','ply_parser.py',62),
  ('program -> declaration Semi','program',2,'p_global_var_single','ply_parser.py',70),
  ('type -> Int','type',1,'p_type','ply_parser.py',77),
  ('function -> type Identifier LParen parameter_list RParen LBrace block RBrace','function',8,'p_function_def','ply_parser.py',85),
  ('function -> type Identifier LParen parameter_list RParen Semi','function',6,'p_function_decl','ply_parser.py',92),
  ('block -> block block_item','block',2,'p_block','ply_parser.py',99),
  ('block -> empty','block',1,'p_block_empty','ply_parser.py',108),
  ('block_item -> statement','block_item',1,'p_block_item','ply_parser.py',115),
  ('block_item -> declaration Semi','block_item',2,'p_block_item','ply_parser.py',116),
  ('statement -> statement_matched','statement',1,'p_statement','ply_parser.py',123),
  ('statement -> statement_unmatched','statement',1,'p_statement','ply_parser.py',124),
  ('statement_matched -> If LParen expression RParen statement_matched Else statement_matched','statement_matched',7,'p_if_else','ply_parser.py',131),
  ('statement_unmatched -> If LParen expression RParen statement_matched Else statement_unmatched','statement_unmatched',7,'p_if_else','ply_parser.py',132),
  ('statement_unmatched -> If LParen expression RParen statement','statement_unmatched',5,'p_if','ply_parser.py',139),
  ('statement_matched -> While LParen expression RParen statement_matched','statement_matched',5,'p_while','ply_parser.py',146),
  ('statement_unmatched -> While LParen expression RParen statement_unmatched','statement_unmatched',5,'p_while','ply_parser.py',147),
  ('statement_matched -> Return expression Semi','statement_matched',3,'p_return','ply_parser.py',154),
  ('statement_matched -> opt_expression Semi','statement_matched',2,'p_expression_statement','ply_parser.py',161),
  ('statement_matched -> LBrace block RBrace','statement_matched',3,'p_block_statement','ply_parser.py',168),
  ('statement_matched -> Break Semi','statement_matched',2,'p_break','ply_parser.py',175),
  ('opt_expression -> expression','opt_expression',1,'p_opt_expression','ply_parser.py',182),
  ('opt_expression -> empty','opt_expression',1,'p_opt_expression_empty','ply_parser.py',189),
  ('declaration -> type Identifier','declaration',2,'p_declaration','ply_parser.py',196),
  ('declaration -> type Identifier Assign expression','declaration',4,'p_declaration_init','ply_parser.py',203),
  ('expression -> assignment','expression',1,'p_expression_precedence','ply_parser.py',210),
  ('assignment -> conditional','assignment',1,'p_expression_precedence','ply_parser.py',211),
  ('conditional -> logical_or','conditional',1,'p_expression_precedence','ply_parser.py',212),
  ('logical_or -> logical_and','logical_or',1,'p_expression_precedence','ply_parser.py',213),
  ('logical_and -> bit_or','logical_and',1,'p_expression_precedence','ply_parser.py',214),
  ('bit_or -> xor','bit_or',1,'p_expression_precedence','ply_parser.py',215),
  ('xor -> bit_and','xor',1,'p_expression_precedence','ply_parser.py',216),
  ('bit_and -> equality','bit_and',1,'p_expression_precedence','ply_parser.py',217),
  ('equality -> relational','equality',1,'p_expression_precedence','ply_parser.py',218),
  ('relational -> additive','relational',1,'p_expression_precedence','ply_parser.py',219),
  ('additive -> multiplicative','additive',1,'p_expression_precedence','ply_parser.py',220),
  ('multiplicative -> unary','multiplicative',1,'p_expression_precedence','ply_parser.py',221),
  ('unary -> postfix','unary',1,'p_expression_precedence','ply_parser.py',222),
  ('postfix -> primary','postfix',1,'p_expression_precedence','ply_parser.py',223),
  ('unary -> Minus unary','unary',2,'p_unary_expression','ply_parser.py',230),
  ('unary -> BitNot unary','unary',2,'p_unary_expression','ply_parser.py',231),
  ('unary -> Not unary','unary',2,'p_unary_expression','ply_parser.py',232),
  ('assignment -> Identifier Assign expression','assignment',3,'p_binary_expression','ply_parser.py',239),
  ('logical_or -> logical_or Or logical_and','logical_or',3,'p_binary_expression','ply_parser.py',240),
  ('logical_and -> logical_and And bit_or','logical_and',3,'p_binary_expression','ply_parser.py',241),
  ('bit_or -> bit_or BitOr xor','bit_or',3,'p_binary_expression','ply_parser.py',242),
  ('xor -> xor Xor bit_and','xor',3,'p_binary_expression','ply_parser.py',243),
  ('bit_and -> bit_and BitAnd equality','bit_and',3,'p_binary_expression','ply_parser.py',244),
  ('equality -> equality NotEqual relational','equality',3,'p_binary_expression','ply_parser.py',245),
  ('equality -> equality Equal relational','equality',3,'p_binary_expression','ply_parser.py',246),
  ('relational -> relational Less additive','relational',3,'p_binary_expression','ply_parser.py',247),
  ('relational -> relational Greater additive','relational',3,'p_binary_expression','ply_parser.py',248),
  ('relational -> relational LessEqual additive','relational',3,'p_binary_expression','ply_parser.py',249),
  ('relational -> relational GreaterEqual additive','relational',3,'p_binary_expression','ply_parser.py',250),
  ('additive -> additive Plus multiplicative','additive',3,'p_binary_expression','ply_parser.py',251),
  ('additive -> additive Minus multiplicative','additive',3,'p_binary_expression','ply_parser.py',252),
  ('multiplicative -> multiplicative Mul unary','multiplicative',3,'p_binary_expression','ply_parser.py',253),
  ('multiplicative -> multiplicative Div unary','multiplicative',3,'p_binary_expression','ply_parser.py',254),
  ('multiplicative -> multiplicative Mod unary','multiplicative',3,'p_binary_expression','ply_parser.py',255),
  ('conditional -> logical_or Question expression Colon conditional','conditional',5,'p_conditional_expression','ply_parser.py',262),
  ('primary -> Integer','primary',1,'p_int_literal_expression','ply_parser.py',269),
  ('primary -> Identifier','primary',1,'p_identifier_expression','ply_parser.py',276),
  ('primary -> LParen expression RParen','primary',3,'p_brace_expression','ply_parser.py',283),
  ('statement_matched -> For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_matched','statement_matched',9,'p_for','ply_parser.py',307),
  ('statement_unmatched -> For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_unmatched','statement_unmatched',9,'p_for','ply_parser.py',308),
  ('statement_matched -> For LParen declaration Semi opt_expression Semi opt_expression RParen statement_matched','statement_matched',9,'p_for','ply_parser.py',309),
  ('statement_unmatched -> For LParen declaration Semi opt_expression Semi opt_expression RParen statement_unmatched','statement_unmatched',9,'p_for','ply_parser.py',310),
  ('statement_matched -> Do statement_matched While LParen expression RParen Semi','statement_matched',7,'p_dowhile','ply_parser.py',317),
  ('statement_unmatched -> Do statement_unmatched While LParen expression RParen Semi','statement_unmatched',7,'p_dowhile','ply_parser.py',318),
  ('statement_matched -> Continue Semi','statement_matched',2,'p_continue','ply_parser.py',325),
  ('parameter_item -> type Identifier','parameter_item',2,'p_parameter_item','ply_parser.py',333),
  ('parameter_list -> parameter_list Comma parameter_item','parameter_list',3,'p_parameter_list','ply_parser.py',341),
  ('parameter_list -> parameter_item','parameter_list',1,'p_parameter_single','ply_parser.py',351),
  ('parameter_list -> empty','parameter_list',1,'p_parameter_empty','ply_parser.py',360),
  ('expression_list -> expression_list Comma expression','expression_list',3,'p_expression_list','ply_parser.py',368),
  ('expression_list -> expression','expression_list',1,'p_expression_single','ply_parser.py',377),
  ('expression_list -> empty','expression_list',1,'p_expression_empty','ply_parser.py',386),
  ('postfix -> Identifier LParen expression_list RParen','postfix',4,'p_call','ply_parser.py',394),
]
