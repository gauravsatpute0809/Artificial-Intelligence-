% -------- PARENT FACTS (ALL TOGETHER) -------- 
 
parent(kashinath, ramraoji). 
parent(meerabai, ramraoji). 
 
parent(ramraoji, pramod). 
parent(jijabai, pramod). 
 
parent(pramod, gaurav). 
parent(sandhya, gaurav). 
 
parent(pramod, xxxx). 
parent(sandhya, xxxx). 
 
% -------- MALE FACTS (ALL TOGETHER) -------- 
 
male(kashinath). 
male(ramraoji). 
male(pramod). 
male(gaurav). 
 
% -------- FEMALE FACTS (ALL TOGETHER) -------- 
 
female(meerabai). 
female(jijabai). 
female(sandhya). 
female(xxxx). 
 
% -------- MARRIAGE FACTS (GROUPED) -------- 
 
husband(kashinath, meerabai). 
husband(ramraoji, jijabai). 
husband(pramod, sandhya). 
 
wife(meerabai, kashinath). 
wife(jijabai, ramraoji). 
wife(sandhya, pramod). 
 
% -------- RULES -------- 
 
father(X, Y) :- 
parent(X, Y), 
male(X). 
 
mother(X, Y) :- 
Artificial Intelligence Lab (N-PCCCS601P) 
Department of Computer Science & Engineering, S.B.J.I.T.M.R., Nagpur 
 
 
 
parent(X, Y), 
female(X). 
 
child(X, Y) :- 
parent(Y, X). 
 
son(X, Y) :- 
child(X, Y), 
male(X). 
 
daughter(X, Y) :- 
child(X, Y), 
female(X). 
 
sibling(X, Y) :- 
parent(Z, X), 
 
parent(Z, Y), 
X \= Y. 
 
grandparent(X, Y) :- 
parent(X, Z), 
parent(Z, Y). 
 
great_grandparent(X, Y) :- 
parent(X, A), 
parent(A, B), 
parent(B, Y). 
 
grandfather(X, Y) :- 
grandparent(X, Y), 
male(X). 
 
grandmother(X, Y) :- 
grandparent(X, Y), 
female(X).