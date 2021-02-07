import React from "react";

import "./App.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Login from "./components/Login/Login.component";
import SignUp from "./components/Login/Signup.component";
import Main from "./components/Main/Main.component";

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route exact path="/" component={Login} />
          <Route exact path="/sign-in" component={Login} />
          <Route exact path="/sign-up" component={SignUp} />
          <Route exact path="/dashbord" component={Main} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;