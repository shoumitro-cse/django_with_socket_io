""""
What is function, subroutine?
We all are familiar with function which is also known as a subroutine, procedure, sub-process, etc. A function is a sequence of instructions packed as a unit to perform a certain task. 

When the logic of a complex function is divided into several self-contained steps that are themselves functions, then these functions are called helper functions or subroutines.

Main function():
   subroutine1()
   subroutine2()
   subroutine3()


Difference between threads and coroutines?
1. In the case of threads, it’s an operating system (or run time environment) that switches between threads according to the scheduler. 

2. In the case of a coroutine, it’s the programmer and programming language which decides when to switch coroutines. Coroutines work cooperatively multitask by suspending and resuming at set points by the programmer. 


Difference between Generators and coroutines?
Ans: In Python, coroutines are similar to generators but with few extra methods and slight changes in how we use yield statements.
Generators produce data for iteration 
coroutines can also consume data. 

In Python 2.5, a slight modification to the yield statement was introduced, now yield can also be used as an expression. For example on the right side of the assignment – 

line = (yield)
whatever value we send to coroutine is captured and returned by (yield) expression. 

A value can be sent to the coroutine by send() method. For example, consider this coroutine which prints out the name having the prefix “Dear” in it. We will send names to coroutine using send() method. 

The execution of the coroutine is similar to the generator. When we call coroutine nothing happens, it runs only in response to the next() and sends () method. This can be seen clearly in the below example, as only after calling __next__() method, our coroutine starts executing. After this call, execution advances to the first yield expression, now execution pauses and waits for the value to be sent to corou object. When the first value is sent to it, it checks for prefix and print name if prefix present. After printing the name, it goes through the loop until it encounters the name = (yield) expression again. 
"""





# Python3 program for demonstrating
# closing a coroutine

def print_name(prefix):
	print("Searching prefix:{}".format(prefix))
	try :
		while True:
			name = (yield)
			if prefix in name:
				print(name)
	except GeneratorExit:
			print("Closing coroutine!!")

corou = print_name("Dear")
corou.__next__()
corou.send("Atul")
corou.send("Dear Atul")
corou.send("Mr Rahim")
corou.send("Dear Korim")
corou.close()

""""
Output:
Searching prefix:Dear
Dear Atul
Dear Korim
Closing coroutine!!
""""


""""
Python3 program for demonstrating coroutine chaining

Chaining coroutines for creating pipeline:

Coroutines can be used to set pipes. We can chain together coroutines and push data through the pipe using send() method. A pipe needs :  

An initial source(producer) derives the whole pipeline. The producer is usually not a coroutine, it’s just a simple method.
A sink, which is the endpoint of the pipe. A sink might collect all data and display it.

source -> coroutine -> coroutine -> coroutine -> sink

Following is a simple example of chaining 
1. producer like as source
2. pattern_filter like as coroutine
3. sink like as sink

producer -> pattern_filter -> sink

"""

def producer(sentence, next_coroutine):
	'''
	Producer which just split strings and
	feed it to pattern_filter coroutine
	'''
	tokens = sentence.split(" ")
	for token in tokens:
		next_coroutine.send(token)
	next_coroutine.close()

def pattern_filter(pattern="ing", next_coroutine=None):
	'''
	Search for pattern in received token
	and if pattern got matched, send it to
	print_token() coroutine for printing
	'''
	print("Searching for {}".format(pattern))
	try:
		while True:
			token = (yield)
			if pattern in token:
				next_coroutine.send(token)
	except GeneratorExit:
		print("Done with filtering!!")

def print_token():
	'''
	Act as a sink, simply print the
	received tokens
	'''
	print("I'm sink, i'll print tokens")
	try:
		while True:
			token = (yield)
			print(token)
	except GeneratorExit:
		print("Done with printing!")

pt = print_token()
pt.__next__()

pf = pattern_filter(next_coroutine = pt)
pf.__next__()

sentence = "Bob is running behind a fast moving car"
producer(sentence, pf)


"""
Output:
I'm sink, i'll print tokens
Searching for ing
running
moving
Done with filtering!!
Done with printing!
"""

