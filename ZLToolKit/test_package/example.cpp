#include <iostream>
#include <Util/MD5.h>

using namespace std;
using namespace toolkit;

int main(int argc, char* argv[]) 
{
	MD5 md5("ZLToolKit");
	cout << "ZLToolKit MD5 is: " << md5.hexdigest() << endl;
    return 0;
}
