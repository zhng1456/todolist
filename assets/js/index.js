var React = require('react')
var ReactDOM = require('react-dom')

//可编辑的区域，包括输入框，与选择框
  class Edit extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        value: '',
      };
      this.submit = this.submit.bind(this);
      this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
      this.setState({
        value: e.target.value,
      })
    }
//提交的方法，这里会去除掉空格，调用taskAdd,使用axios,向后台提交
    submit(e) {
      e.preventDefault();
      let task = ReactDOM.findDOMNode(this.refs.textInput).value.trim();
      let priority=ReactDOM.findDOMNode(this.refs.prioritySelect).value.trim();
      if(!task){
        return ;
      }
      //调用taskAdd后台添加
      this.props.taskAdd(task,priority);
      //输入框置空
      this.setState({
        value: "",
      })
    }

    render() {
      return (
        <div>
          <input ref="textInput" className="form-control" type="text" value={this.state.value} onChange={this.handleChange} placeholder="input please"/>
          <div className="text-left">
            <label for="name">优先级</label>
            <select class="form-control" ref="prioritySelect">
			<option value="1">正常</option>
			<option value="2">重要</option>
			<option value="3">紧急</option>
		    </select>
          </div>
          <div className="text-right">
            <button className="btn btn-success" onClick={this.submit}>commit</button>
          </div>
        </div>
      )
    }
  }
  //排序方法的下拉列表
  class SortSelect extends React.Component{
    constructor(props) {
      super(props);
      this.taskSort = this.taskSort.
      bind(this);
    }
    taskSort(e) {
      this.props.taskSort(e.target.value);
    }
    render() {
      return (
      <div className="text-left">
        <label for="name">sorted by</label>
        <select class="form-control" ref="sortRule" onChange={this.taskSort}>
        <option value="0" selected="selected">id</option>
        <option value="1">priority</option>
        </select>
      </div>
      )
    }
  }
  class ListItem extends React.Component {
    constructor(props){
      super(props);
      this.deleteTask = this.deleteTask.bind(this);
      this.toggleChange = this.toggleChange.bind(this);
      this.taskChange = this.taskChange.
      bind(this);
    }

    deleteTask() {
      console.log(this.props);
      this.props.deleteTask(this.props.taskId);
    }

    toggleChange() {
      this.props.toggleComplete(this.props.taskId);
    }

    taskChange(e) {
      this.props.taskChange(this.props.taskId, e.target.value);
    }

    render() {
      let task = this.props.task;
      let itemChecked = false;
      let classes = "list-group-item";
      if(this.props.complete === true){
        task = (<del>{task}</del>);
        itemChecked = true;
        classes += " list-group-item-success"
      } else {
        task = (
          <input type="text" onChange={this.taskChange} value={task} />
        )
      }


      return (
        <li className={classes}>
          <div>
            <input type="checkbox" className="pull-left" checked={itemChecked} onChange={this.toggleChange} />
            {task}
            <div className="text-left">
            <label for="name">优先级</label>
            {this.props.priority}
          </div>
            <button className="btn btn-danger pull-right" onClick={this.deleteTask}>delete</button>
          </div>
        </li>
      )
    }
  }

  class List extends React.Component {
    render() {
      return (
        <ul className="list-group">
          {this.props.data.map(
            listItem => (
              <ListItem
                task={listItem.task}
                taskId={listItem.id}
                complete={listItem.complete}
                priority={listItem.priority}
                deleteTask={this.props.deleteTask}
                toggleComplete={this.props.toggleComplete}
                taskChange={this.props.taskChange}/>
            )
          )}
        </ul>
      )
    }
  }

  class Main extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
          data: [],
      };
      this.init();
      this.taskAdd = this.taskAdd.bind(this);
      this.taskRemove = this.taskRemove.bind(this);
      this.taskToggleComplete = this.taskToggleComplete.bind(this);
      this.taskChange = this.taskChange.bind(this);
      //新增的taskSort
      this.taskSort = this.taskSort.bind(this);
    }

    init() {
      axios.get('/list/api/msg/').then(
        res => {
          this.setState({
            data: res.data,
          });
        }
      );
    }
    taskSort(flag) {
      console.log('sort rules: '+flag)
      axios.get('/list/api/msg-order/'+flag).then(
        res => {
          this.setState({
            data: res.data,
          });
        }
      );
    }
    getId() {
      let id=0;
      let dataTemp = this.state.data;
      for(let item1 in dataTemp){
        id = Math.max(id, dataTemp[item1].id + 1);
      }
      return id;
    }
//添加一个任务
    taskAdd(taskTemp,priority) {
      let dataTemp = {};
      dataTemp['id'] = this.getId();
      dataTemp['task'] = taskTemp;
      dataTemp['complete'] = false;//默认的complete标志位为0
      dataTemp['priority']=parseInt(priority);//设置对应的优先级
      axios.post('/list/api/msg/', dataTemp).then(
        res => {
          this.setState({
            data: this.state.data.concat(res.data),
          });
        }
      );
    }

    taskRemove(taskId) {
       axios.delete('/list/api/msg/' + taskId).then(
        res => {
          if(res.data['complete']) {
            let dataTemp = this.state.data;
            dataTemp = dataTemp.filter(function (task) {
              return task.id !== taskId;
            });
            this.setState({
              data:dataTemp,
            })
          }
        }
      );
    }
//完成任务的方法
    taskToggleComplete(taskId) {
      let dataTemp = this.state.data;
      let item = {
        'complete': false,
      };
      for(let i in dataTemp){
        if(dataTemp[i].id === taskId){
          dataTemp[i].complete = dataTemp[i].complete === true ? false : true;
          item['complete'] = dataTemp[i].complete;
          break;
        }
      }
      this.setState({
        data: dataTemp,
      });
      axios.put('/list/api/msg/' + taskId, item).then(
        res => {}
      );
    }

    taskChange(id, task) {
      let dataTemp = this.state.data;
      for(let item in dataTemp) {
        if(dataTemp[item].id === id) {
          dataTemp[item].task = task;
        }
      }
      this.setState({
        data: dataTemp,
      });

      let item = {
        'task': task,
      };
      console.log(task);
      axios.put('/list/api/msg/' + id, item).then(
        res => {}
      );
    }

    render() {
      return (
        <div className="col-md-6 col-md-offset-3">
          <Edit
            taskAdd={this.taskAdd} />
          <hr/>
          <SortSelect taskSort={this.taskSort}/>
          <List
            data={this.state.data}
            deleteTask={this.taskRemove}
            toggleComplete={this.taskToggleComplete}
            taskChange={this.taskChange}/>
        </div>
      )
    }
  }

  ReactDOM.render(
    <Main />,
    document.getElementById('container')
  )