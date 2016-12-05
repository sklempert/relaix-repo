Index: bin/control_rancid.in
===================================================================
--- bin/control_rancid.in	(revision 3116)
+++ bin/control_rancid.in	(working copy)
@@ -206,13 +206,14 @@
 routers.down
 routers.up
 EOF
+    fi
     if [ ! -f configs/.cvsignore ] ; then
 	rm -rf configs/.cvsignore
-	cat > configs/.cvsignore <<EOF
+	cat > configs/.cvsignore <<EOF2
 .old
 *.new
 *.raw
-EOF
+EOF2
     fi
     if [ $RCSSYS = svn ] ; then
 	svn propset svn:ignore -F .cvsignore .
@@ -219,7 +220,6 @@
 	svn propset svn:ignore -F configs/.cvsignore configs
 	svn update .
 	svn commit -m 'set svn:ignores' .
-	fi
     fi
     ;;
 esac
Index: bin/control_rancid.in
===================================================================
--- bin/control_rancid.in	(revision 3123)
+++ bin/control_rancid.in	(working copy)
@@ -449,7 +449,7 @@
 done
 echo
 # delete configs from RCS for routers not listed in routers.up.
-for router in `find . \( -name \*.new -prune -o -name CVS -prune -o -name .svn -prune -o -name .gitignore -prune \) -o -type f -print | sed -e 's/^.\///'` ; do
+for router in `find . \( -name \*.new -prune -o -name CVS -prune -o -name .svn -prune -o -name .cvsignore -prune -o -name .gitignore -prune \) -o -type f -print | sed -e 's/^.\///'` ; do
     grep -i "^$router\;" ../router.db > /dev/null 2>&1
     if [ $? -eq 1 ] ; then
 	rm -f $router
