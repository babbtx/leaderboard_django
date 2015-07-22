(function(root, $){
  'use strict';

  function toInt(value){
    return parseInt('' + value);
  }

  /* converts array of objects {name: ex1, score: val1} to hash {ex1: val1} */
  function createLeadersHash(leaders){
    var result = {};
    if (typeof(leaders.slice) !== 'function'){
      leaders = [leaders];
    }
    $.each(leaders, function(_,leader){
      result[leader.name] = toInt(leader.score);
    });
    return result;
  }

  /**
    * Maintains a leaderboard of names ans scores in memory and persists to the server.
    *
    * Initialize with company identifier and array of leader objects {name: ..., score: ...}.
    *
    * Add values with add().
    *
    * Subscribe to events 'updated' and 'added'.
    */
  function Leaderboard(uid, leaders){
    this.uid = uid;
    this.leaders = createLeadersHash(leaders);
    this.eventsDelegate = $({});
  };

  Leaderboard.prototype = {

    /*
     * Internal.
     */
    _update: function(data){
      var _this = this;
      var updatedLeaders = [];
      var addedLeaders = [];
      $.each(data, function(_,leader){
        if (typeof(_this.leaders[leader.name]) === 'undefined'){
          addedLeaders.push(leader);
        }
        else if (_this.leaders[leader.name] !== toInt(leader.score)){
          updatedLeaders.push(leader);
        }
        _this.leaders[leader.name] = toInt(leader.score);
      });
      if (updatedLeaders.length > 0){
        this._trigger('updated', updatedLeaders);
      }
      if (addedLeaders.length > 0){
        this._trigger('added', addedLeaders);
      }
      return this.leaders;
    },

    /*
     * Internal.
     */
    _trigger: function(){
      var args = [].slice.call(arguments, 0);
      args[1] = [ args[1] ]; // because jquery expands the array, we wrap the array in an array
      return this.eventsDelegate.trigger.apply(this.eventsDelegate, args);
    },

    /**
     * Takes array of objects {name: ..., score: ...} to incrementally add to the leaderboard.
     * Triggers events 'added' or 'updated' with the resulting (total) score per leader.
     */
    add: function(adds){
      var _this = this;
      if (typeof(adds.slice) !== 'function'){
        adds = [adds];
      }
      $.ajax({
        url: '/leaderboard/' + this.uid + '/',
        data: JSON.stringify(adds),
        contentType: 'application/json',
        dataType: 'JSON',
        method: 'POST',
        headers: {'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')},
      })
      .done(function(data){
        _this._update(data);
      });
    },

    /**
     * Events:
     * 'added':     Event triggered when add() has been processed. Argument is the array of added leaders in the form {name: ..., score: ...}.
     * 'updated':   Event triggered when add() has been processed. Argument is the array of updated leaders in the form {name: ..., score: ...}.
     */
    on: function(){
      return this.eventsDelegate.on.apply(this.eventsDelegate, arguments);
    },
  };

  root.Leaderboard = Leaderboard;
})(this, jQuery);
