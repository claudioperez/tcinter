#ifndef TKINTER_H
#define TKINTER_H
/* cmp  **************************************/
#ifndef Py_TPFLAGS_DISALLOW_INSTANTIATION
#  define Py_TPFLAGS_DISALLOW_INSTANTIATION (1UL << 7)
#endif
#ifndef Py_IS_TYPE
#  define Py_IS_TYPE(obj, typ) (Py_TYPE(obj) == typ)
#endif
/*********************************************/




/* This header is used to share some macros between _tkinter.c and
 * tkappinit.c.
 * Be sure to include tk.h before including this header so
 * TK_HEX_VERSION is properly defined. */

/* TK_RELEASE_LEVEL is always one of the following:
 *  TCL_ALPHA_RELEASE   0
 *  TCL_BETA_RELEASE    1
 *  TCL_FINAL_RELEASE   2
 */
#define TK_HEX_VERSION ((TK_MAJOR_VERSION << 24) | \
                        (TK_MINOR_VERSION << 16) | \
                        (TK_RELEASE_LEVEL << 8) | \
                        (TK_RELEASE_SERIAL << 0))

/* Protect Tk 8.4.13 and older from a deadlock that happens when trying
 * to load tk after a failed attempt. */
#if TK_HEX_VERSION < 0x0804020e
#define TKINTER_PROTECT_LOADTK
#define TKINTER_LOADTK_ERRMSG \
        "Calling Tk_Init again after a previous call failed might deadlock"
#endif

#endif /* !TKINTER_H */
