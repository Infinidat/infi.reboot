#include <utmpx.h>

int aix_uptime()
{
    int nBootTime = 0;
    int nCurrentTime = time(NULL);
    struct utmpx * ent;

    setutxent();
    while ((ent = getutxent())) {
        if (!strcmp("system boot", ent->ut_line)) {
            nBootTime = ent->ut_tv.tv_sec;
            break;
        }
    }
    endutxent();
    return nCurrentTime - nBootTime;
}
