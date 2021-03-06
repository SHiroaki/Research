#include <Python.h>

#define LOWER_BOUND    0
#define UPPER_BOUND    1000
#define MAX_BIT_LENGTH 7

int binaryToValue(int *);

static PyObject *
valueToBinary(PyObject *self, PyObject *args)
{
  //return gray code
  int i, n, m, len;
  unsigned int num;
  int b[MAX_BIT_LENGTH];
  PyListObject *binary;
  binary = (PyListObject *) PyList_New(MAX_BIT_LENGTH);

  if (!PyArg_ParseTuple(args, "i", &num)){
    return NULL;
  }
  //n = (num >> 1) ^ num; //gray codeに変換

  //2進数に変換
  for (i=0; n>0; i++){
    m=n%2;   //2で割ったあまり
    n=n/2;  //2で割る
    b[i] = m;
  }

  len = i; //整数の2進数変換した時の長さ

  //10bitになるようにけつに0を追加する
  for (i=len; i<MAX_BIT_LENGTH; i++ ){
    b[i] = 0;
  }
 
  //逆順だったビット列を2進数の順にコピーする
  n = 0;
  for (i=MAX_BIT_LENGTH-1; i>=0; i--){
  //gray に1bitずつint型の値を入れていく
    PyList_SET_ITEM(binary, n++, Py_BuildValue("i", b[i]));
  }

  return Py_BuildValue("O", binary);
}


static PyObject *
make_individual(PyObject *self, PyObject *args)
{

  int b[MAX_BIT_LENGTH];
  int m,n,i,len;
  unsigned int p;

  PyListObject *gray; //pythonのlistオブジェクトを表現
  gray = (PyListObject *) PyList_New(MAX_BIT_LENGTH); //サイズがMAX~のリストを作る

  if (!PyArg_ParseTuple(args, "i", &p)){ //引数が複数の時はiiみたいに並べて書く
    return NULL;
  }

  n = p;
  //2進数に変換
  for (i=0; n>0; i++){
    m=n%2;   //2で割ったあまり
    n=n/2;  //2で割る
    b[i] = m;
  }

  len = i; //整数の2進数変換した時の長さ

  //10bitになるようにけつに0を追加する
  for (i=len; i<MAX_BIT_LENGTH; i++ ){
    b[i] = 0;
  }
 
  //逆順だったビット列を2進数の順にコピーする
  n = 0;
  for (i=MAX_BIT_LENGTH-1; i>=0; i--){
  //gray に1bitずつint型の値を入れていく
    PyList_SET_ITEM(gray, n++, Py_BuildValue("i", b[i]));
  }

  return Py_BuildValue("O", gray);
}

static PyObject *
grayToBinary(PyObject *self, PyObject *args)
{

  unsigned int num;
  unsigned int mask;
  int m,n,i,len;
  int b[MAX_BIT_LENGTH], inputed_binary[MAX_BIT_LENGTH];
  PyListObject *binary; //pythonのlistオブジェクトを表現
  PyObject *get_list;
  binary = (PyListObject *) PyList_New(MAX_BIT_LENGTH); 

  if (!PyArg_ParseTuple(args, "O", &get_list )){
    return NULL;
  }
  if PyList_Check(get_list) {
      for (i=0; i<PyList_Size(get_list); i++){
	//リストオブジェクトの中身をCで見れるように変換しながら取り出す?(自信なし)
	inputed_binary[i] = PyInt_AsSsize_t(PyList_GetItem(get_list, (Py_ssize_t)i)); //ok
      }
    }
  
  num = binaryToValue(inputed_binary);
  
  for (mask = num >> 1; mask != 0; mask = mask >> 1){
    //gray codeから元に戻す
    num = num ^ mask;
  }
  
  n = num;
  //2進数に変換
  for (i=0; n>0; i++){
    m=n%2;   //2で割ったあまり
    n=n/2;  //2で割る
    b[i] = m;
  }

  len = i; //整数の2進数変換した時の長さ

  //10bitになるようにけつに0を追加する
  for (i=len; i<MAX_BIT_LENGTH; i++ ){
    b[i] = 0;
  }
  
  //逆順だったビット列を2進数の順にコピーする
  n = 0;
  for (i=MAX_BIT_LENGTH-1; i>=0; i--){
    //binary に1bitずつint型の値を入れていく
    PyList_SET_ITEM(binary, n++, Py_BuildValue("i", b[i]));
  }

  return Py_BuildValue("O", binary);
}


int binaryToValue(int *b){
  //2進数を整数に変換する
  int i,n;
  i=0; n=0;

  while(i < MAX_BIT_LENGTH){
    if (b[i] == 1) n+=1;
    i+=1;
    if (i == MAX_BIT_LENGTH) break;
    n=n*2;
    //printf("%d\n", n);
  }
  return n;
}

static PyObject *
binaryToPtype(PyObject *self, PyObject *args)
{

  int i,n;
  int inputed_binary[MAX_BIT_LENGTH];
  PyListObject *binary; //pythonのlistオブジェクトを表現
  PyObject *get_list;

  if (!PyArg_ParseTuple(args, "O", &get_list )){ //pythonオブジェクトをそのまま渡す
    return NULL;
  }
  
  if PyList_Check(get_list) {
      for (i=0; i<PyList_Size(get_list); i++){
	inputed_binary[i] = PyInt_AsSsize_t(PyList_GetItem(get_list, (Py_ssize_t)i)); //ok
      }
    }
  
  i=0; n=0;

  while(i < MAX_BIT_LENGTH){
    if (inputed_binary[i] == 1) n+=1;
    i+=1;
    if (i == MAX_BIT_LENGTH) break;
    n=n*2;
    //printf("%d\n", n);
  }
  return Py_BuildValue("i", n);
}


static PyObject *
hello(PyObject *self)
{
    printf("Hello World!!\n");
    Py_RETURN_NONE;
}

static char ext_doc[] = "C extention module example\n";

static PyMethodDef methods[] = {
  {"value2binary", make_individual, METH_VARARGS, "return gray code.\n"},
  {"binary2value", binaryToPtype, METH_VARARGS, "return ptype value.\n"},
  {NULL, NULL, 0, NULL}
};

void initcbinarymethods(void)
{
  (void) Py_InitModule("cbinarymethods", methods);
}
