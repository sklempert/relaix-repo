Index: etc/rancid.types.base
===================================================================
--- etc/rancid.types.base	(revision 3076)
+++ etc/rancid.types.base	(working copy)
@@ -7,22 +7,23 @@
 #
 agm;script;agmrancid
 #
-adtran;script;rancid -t adtran
-adtran;module;adtran
-adtran;inloop;adtran::inloop
-adtran;login;clogin
+# XXX This was the start of support for adtran, but it is incomplete.
+#adtran;script;rancid -t adtran
+#adtran;module;adtran
+#adtran;inloop;adtran::inloop
+#adtran;login;clogin
 # TA5000
-adtran;command;adtran::ShowVersion;show version
-adtran;command;adtran::ShowSystemInventory;show system inventory
-adtran;command;adtran::ShowTableInterfaces;show table interfaces
-adtran;command;adtran::ShowEvc;show evc
-adtran;command;adtran::ShowEvcmap;show evc-map
-adtran;command;adtran::ShowEfmgroup;show efm-group 1
-adtran;command;adtran::ShowInterfacesShdsl;show interfaces shdsl
-adtran;command;adtran::ShowInterfacesAdsl;show interfaces adsl
+#adtran;command;adtran::ShowVersion;show version
+#adtran;command;adtran::ShowSystemInventory;show system inventory
+#adtran;command;adtran::ShowTableInterfaces;show table interfaces
+#adtran;command;adtran::ShowEvc;show evc
+#adtran;command;adtran::ShowEvcmap;show evc-map
+#adtran;command;adtran::ShowEfmgroup;show efm-group 1
+#adtran;command;adtran::ShowInterfacesShdsl;show interfaces shdsl
+#adtran;command;adtran::ShowInterfacesAdsl;show interfaces adsl
 # EFM NTU
-adtran;command;adtran::ShowInterfaces;show interfaces
-adtran;command;adtran::WriteTerm;show running-config
+#adtran;command;adtran::ShowInterfaces;show interfaces
+#adtran;command;adtran::WriteTerm;show running-config
 #
 alteon;script;arancid
 alteon;login;alogin
