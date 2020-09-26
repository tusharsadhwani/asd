import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class AuthUser extends ChangeNotifier {
  bool _isLoggedIn;
  bool get isLoggedIn => _isLoggedIn;

  AuthUser() {
    _isLoggedIn = false;
  }

  void login() {
    _isLoggedIn = true;
    notifyListeners();
  }

  void signOut() {
    _isLoggedIn = false;
    notifyListeners();
  }
}

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AuthUser(),
      builder: (_, __) => Consumer<AuthUser>(
        builder: (_, authUser, __) {
          if (authUser.isLoggedIn) {
            return MaterialApp(
              home: LoggedInPage(),
            );
          }
          return MaterialApp(
            home: LoggedOutPage(),
          );
        },
      ),
    );
  }
}

class LoggedInPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.blue,
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Logged in!'),
              Consumer<AuthUser>(
                builder: (_, authUser, __) => RaisedButton(
                  onPressed: authUser.signOut,
                  child: Text('Sign out'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class LoggedOutPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.red,
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Logged out!'),
              Consumer<AuthUser>(
                builder: (_, authUser, __) => RaisedButton(
                  onPressed: authUser.login,
                  child: Text('Log in'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
