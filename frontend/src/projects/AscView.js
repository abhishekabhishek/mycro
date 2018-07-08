import React, { Component } from 'react';
import {ascAddressToJson, getProjectForAddress} from './ProjectHelpers.js';

class Asc extends Component {
  constructor(props) {
    super(props);

    this.state = {
      projectContract: null,
      asc: this.getAsc(this.props.match.params.ascId),
      voteState: "NOT_VOTED",
    }


    this.loadAsc(this.props.match.params.ascId);
    getProjectForAddress(this.props.match.params.projectId).then(projectContract => {
      this.setState(Object.assign(this.state, {projectContract}));

      this.loadVoteState();
    });
  }
  loadVoteState(){
    this.state.projectContract.get_asc_votes(this.state.asc.id, this.state.asc.id).then(votes => {
      console.log(votes);
      if(votes.find(address => address === window.web3.eth.defaultAccount)){
      
        this.setState(Object.assign(this.state, {voteState: "VOTE_ACCEPT"}));
      }
    });
  }

  getAsc(id){
    return {
        id,
        name: "appoint baz",
        code: "some code\n contract foo\nbar\nbaz\n"
      }
  }

  loadAsc(id){
    ascAddressToJson(id).then((asc) => {
      asc.code = "foo bar baz delete me";

      this.setState(Object.assign(this.state, {asc}));
    });
  }

  voteAccept(){
    this.state.projectContract.vote(this.state.asc.id).then(() =>{
      this.loadVoteState();
    });
  }

  voteReject(){
    this.updateVoteState("VOTE_REJECT");
  }

  updateVoteState(newVoteState){
    const oldState = this.state;
    const newState = Object.assign({...oldState}, {voteState: newVoteState});
    this.setState(newState);
  }

  render() {
    const asc = this.state.asc;
    const Footer = (props) => {
      switch(this.state.voteState) {
        case "VOTE_ACCEPT":
          return (<h1>You voted to accept</h1>)
        case "VOTE_REJECT":
          return (<h1>You voted to reject</h1>)
        default:
          return (
            <div>
              <button onClick={() => this.voteAccept()}>Vote Accept</button>
              <button onClick={() => this.voteReject()}>Vote Reject</button>
            </div>
          )
      }
    }
    return (
      <div className="Page">
        <h1>Asc {asc.name}</h1>
        <div>
          {asc.code}
        </div>
        <Footer/>
      </div>
    );
  }
}

export default Asc;
