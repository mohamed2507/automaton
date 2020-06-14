# automaton
**french language is used in the program instead of english for pedagogical reasons**
**you need to install graphviz**
## Automaton Creation
### States
To define a state we use this syntax :Etat("name of the state",unique id {int})
### Transitions 
Transitions must be in this format : [[state1,letter,state2],[state3,letter,state4].........]
### Automaton
**Initial state must be a single element wheras final state is a list of states**
Automate(alphabet,initial state,final states,states,transitions)
## Operations
## Display
you can display your automaton using the function **show** with the following syntax: automaton.show(name of the automate).
a folder by the name **automate** where you will find your automaton in **PDF** file.
## Mirror 
you can transform your automaton into its mirror using the function **mirror** with the following syntax: automaton.mirror()
## Reduction
you can remove all no accessible elements and no co-accessible elements in your automaton  using the function **reduction** with the following syntax: automaton.reduction()
##  Eliminate epsilon transitions 
you can remove all epsilon transitions in your automaton  using the function **elemination_epsilon** with the following syntax: automaton.elemination_epsilon()
##  Deterministe
you can transform your automaton into a determinist automaton using the function **deterministe** with the following syntax: automaton.deterministe()
##  Complete
you can transform your automaton into a complete automaton using the function **complet** with the following syntax: automaton.complet()
##  Complement
you can transform your automaton into a complement automaton using the function **complement** with the following syntax: automaton.complement()
## Recognition of words
using the function **reconnait** you can check if a word is recognized by this automaton using the following syntax: automaton.reconnait(word)
## Check if an automaton is determinsit
using the following syntax: automaton.est_determinist()
## Simplify 
sometimes when using the determinist operation the states of the new automaton will be composed of multiple simple states ,this operation will help to transform  complex states into simple ones ex: [state1,state2,state3]--->state4.using the following synatx : automaton.simplify()
## check if an automaton is complete 
using the following synatx :automaton.is_complet()
