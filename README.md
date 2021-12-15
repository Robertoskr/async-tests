<h1>Simple async tests</h1>
This is a simple script for running your python tests asynchronously,
its compatible with python unittest test, i didnt prove it with any other testing library.

<h2>How to use it?<h2>
Simply call it : python runtests.py

<h2>Tips</h2>
In test/base.py you have a base class that inherits from Unittest.TestCase, you can design your setUp, tearDown
functions for achieving the funcionality that you want, and declare your own information on the __init__() function

<h2>Example</h2>

```
class MyBase(BaseTest):
  def __init__(self):
    self.someinfo = 5
    self.someotherinfo = 9
    super(MyBase, self).__init__()
   
  def setUp(self):
    print("this runs before each test")
   
  def tearDown(self):
    print("this runs after each test")

class TestExample(BaseTest):
  def test_should_sum_two_nums(self):
    self.assertEqual(5, sum(2, 3))
    self.assertTrue(myOwnFunction(some_input))
    #you can use native python assert
    assert 5 == 7 #this raises an AssertionError
   
  def test_something(self):
    assert this_function() == this_other_function()
    
THEN
python3 runtests.py
    
```

<h3> And that's all </h3>
