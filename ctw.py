#-----------------------------------------------------------
# Author: Gabriel Hofer
#-----------------------------------------------------------
class ctw:
  # build the tree
  def __init__(self,s,d):
    self.seq, self.depth, self.n, self.tree, self.Pw = s, d, len(s), {}, {}
    self.tree['root']=[0,0] 
    for i in range(d,len(s)):
      for j in range(0,d+1):
        context= 'root' if j==0 else s[i-j:i]
        if context not in self.tree: self.tree[context]=[0,0]
        self.tree[context][int(s[i:i+1])]+=int(1)

  # get next symbol and update context path
  def addSymbol(self,b):
    self.tree['root'][int(b)]+=int(1)
    for i in range(1,self.depth+1):
      context=self.seq[self.n-i:]
      if context not in self.tree:
        self.tree[context]=[0,0]
      self.tree[context][int(b)]+=int(1)
    self.seq+=b
    self.n+=1

  # prints the tree and a, b
  def showTree(self):
    for i in self.tree: 
      print(i+" --> "+str(self.tree[i]))

  # prints the current sequence
  def showSource(self): 
    print(self.seq)

  # Krichevsky–Trofimov estimator
  def Pe(self,a,b):
    if a: return ((a-0.5)/(a+b))*self.Pe(a-1,b)
    elif b: return ((b-0.5)/(a+b))*self.Pe(a,b-1)
    else: return 1

  # calculate probabilities for nodes in the tree
  def probs(self,s):
    [a,b] = self.tree[s] if s in self.tree else [0,0]
    if s=='': [a,b]=self.tree['root']
    if(len(s)==self.depth):
      self.Pw[s]=self.Pe(a,b)
    else:
      self.probs('0'+s)
      self.probs('1'+s)
      self.Pw[s] = (self.Pe(a,b) + self.Pw['0'+s] * self.Pw['1'+s])/2

  # prints all probabilities of nodes in the tree
  def showProbs(self):
    for i,j in self.Pw.items():
      print(i+"   Pw: "+str(j))

#-----------------------------------------------------------
# Demo
#-----------------------------------------------------------
def demo():
  sequence = "1100100110"
  t = ctw(sequence,3)
  print('Context-Tree\n---------------------------')
  t.showTree()
  print('Probabilities & Weights\n---------------------------')
  t.probs('')
  t.showProbs()
  
  print('Added a symbol\n---------------------------')
  t.addSymbol('1')
  t.showTree()

demo()

