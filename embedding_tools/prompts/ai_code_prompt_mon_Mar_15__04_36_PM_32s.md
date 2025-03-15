# User Request:
# Project Plan
We are enhancing the log viewer system that we already have.  We already have many of the web components and code working but we want to start to add new features.
## What we want to add:
- When the web page starts up:
  - Read the monitored objects table to get the relevant objects that need to be viewed.
  - Create a web component for each object.
  - Insert the web components in the order they should be run.

- Web component behavior:
  - Initially, set all components to white.
  - Change them to yellow when they are running.
  - If a component fails:
    - Turn it red.
    - Halt all testing.

- After the test is finished, provide five buttons:
  - **Run Next Test**
  - **Run This Test Again**
  - **Run Previous Test**
  - **Run The 1st Test**
  - **Run All Tests**

- Before running the next test:
  - Ensure that the web components from the last test are cleared from the display.

- Additional feature:
  - A text box below should display the output of the Python script orchestrating all of the tests.

# Your Task
List all of the objects needed to create this new system.  Use the existing objects and Interfaces where ever possible.  For example, we have an accordion component that should be used for each row that is pulled from the table and has log information in it.
# Relevant Code:
```typescript
class LogViewer implements IWebComponent {
    static observedAttributes() {} // return an array containing the names of the attributes you want to observe
    
    $log_viewer_container  !: HTMLElement;      //   <div class="screen-area"> 
	$object_name_header    !: HTMLElement;      //       <h1 class="object-name"></h1>
	$list_of_log_objects   !: HTMLElement;      //       <div class="list-of-log-objects"></div>
    $cloneable_log_object  !: HTMLElement;      //       <log-object class="cloneable-log-object">terminal ready.
                                                //       <!-- clone me --></log-object>
                                                //   </div>
    object_name:          string       = "";  
    // logs:                 ILogObject[] = [];
    monitored_object_id:  string       = "";
    data_source_location: string       = "";
    log_length:           number       =  0;
    logObjectContainerSource!: LogObjectContainerSource;
    
    

    get logs() {
        console.log( 'logs read' );
        return [];
    }
    
    set logs( logObjects: ILogObject[]) {
        // console.log('prop written, new value', logObjects );
        if ( logObjects.length !== this.log_length ) { 
            console.log( "length changed! "); 
            this.log_length = logObjects.length;
            this.displayLogObjects( logObjects, this );
        }
    }  
    constructor( private $el: HTMLElement, private $host: Element ) {
        this.data_source_location = $host.getAttribute( "data_source_location" )!, 
        this.monitored_object_id  = $host.getAttribute( "monitored_object_id"  )! 
    }

    /**
     * Invoked each time the custom element is appended into a document-connected element.
     * This will happen each time the node is moved, and may happen before the element's contents have been fully parsed.
     */
    connectedCallback() {
        // console.log( 'defining log viewer elements...' );
        this.$log_viewer_container = this.$el.querySelector(                   ".screen-area"          )!;
        this.$object_name_header   = this.$log_viewer_container.querySelector( ".object-name"          )!;
        this.$list_of_log_objects  = this.$log_viewer_container.querySelector( ".list-of-log-objects"  )!;
        // this.$object_name_header.innerHTML = this.monitored_object_id;
        const logObjectSourceConfiguration = new SourceConfig( "url", this.data_source_location, this.monitored_object_id );
        this.logObjectContainerSource      = new LogObjectContainerSource( logObjectSourceConfiguration );
        this.start();
    }

    disconnectedCallback() { console.log( 'log-viewer disconnected' ); }
    adoptedCallback() {      console.log(      'log-viewer moved'   ); }

    /**
     * Invoked each time one of the custom element's attributes is added, removed, or changed.
     * Which attributes to notice change for is specified in a static get observedAttributes method
     *
     * @param name
     * @param oldValue
     * @param newValue
     */
    attributeChangedCallback( name: string, oldValue: any, newValue: any ) {
        const nameProp = name.replace( /-[a-zA-Z]/g, ( found: string ) => found.slice( 1 ).toUpperCase() );
        ( this as any )[ nameProp ] = newValue; }

    start() {
        setInterval(() => { 
            // console.log( "refreshing logs... " );
            this.logObjectContainerSource.refresh();
            this.logs = this.logObjectContainerSource.logObjectProcessor.getWrittenLogs(); }, 1000 ); }

    displayLogObjects( logObjects: ILogObject[], logViewer: LogViewer ) {
        console.log( "displaying log objects..." );
        logObjects.forEach( log_object => {
            let formatted_time_stamp = new Date( log_object?.timestamp ).toLocaleString()
            let li_inner_html = `
                <div class="log-object-container">
                    <div class="timestamp">${ formatted_time_stamp }</div>
                    <div class="method"   >${ log_object.method    }</div>
                    <div class="message"  >${ log_object.message   }</div>
                </div>`;
            let $new_list_element = document.createElement( 'li' );
            $new_list_element.innerHTML = li_inner_html;
            this.$list_of_log_objects.appendChild( $new_list_element );
        });
    }
}
```
```typescript
connectedCallback() {
        // console.log( 'defining log viewer elements...' );
        this.$log_viewer_container = this.$el.querySelector(                   ".screen-area"          )!;
        this.$object_name_header   = this.$log_viewer_container.querySelector( ".object-name"          )!;
        this.$list_of_log_objects  = this.$log_viewer_container.querySelector( ".list-of-log-objects"  )!;
        // this.$object_name_header.innerHTML = this.monitored_object_id;
        const logObjectSourceConfiguration = new SourceConfig( "url", this.data_source_location, this.monitored_object_id );
        this.logObjectContainerSource      = new LogObjectContainerSource( logObjectSourceConfiguration );
        this.start();
    }
```
```typescript
displayLogObjects( logObjects: ILogObject[], logViewer: LogViewer ) {
        console.log( "displaying log objects..." );
        logObjects.forEach( log_object => {
            let formatted_time_stamp = new Date( log_object?.timestamp ).toLocaleString()
            let li_inner_html = `
                <div class="log-object-container">
                    <div class="timestamp">${ formatted_time_stamp }</div>
                    <div class="method"   >${ log_object.method    }</div>
                    <div class="message"  >${ log_object.message   }</div>
                </div>`;
            let $new_list_element = document.createElement( 'li' );
            $new_list_element.innerHTML = li_inner_html;
            this.$list_of_log_objects.appendChild( $new_list_element );
        });
    }
```
```typescript
class MonitoredObject {
    object_view_id:     string;
    logObjects:         ILogObject[];
    model:              Model;
    logObjectFactory:   LogObjectFactory;
    monitorLed:         MonitorLed;
    stringifier:        Stringifier;
    constructor( config: { new_id: string | null, data_source_location: string | null; } ) {
        if ( config.new_id?.length === 0 ) { config.new_id = Math.floor( Math.random() * 1000 + 1000 ).toString(); }
        if ( config.new_id?.includes('_')) {
            this.object_view_id = config.new_id
        } else { this.object_view_id = `${ this.constructor.name }_${ config.new_id }`; }
        this.logObjectFactory  = new LogObjectFactory();
        this.logObjects        = [ this.logObjectFactory.createLogObject( "constructing...", this )];
        if ( config.data_source_location?.length === 0 && document.querySelector( '.data-source-location' )) { 
            config.data_source_location = document.querySelector( '.data-source-location' )?.innerHTML || "" }
        this.model             = new Model( new SourceData({ Runner: FetchRunner, url: config.data_source_location! }));
        this.monitorLed        = new MonitorLed();
        this.stringifier       = new Stringifier();
        const data_config        = { object_view_id: this.object_view_id, object_data: this.stringifier.stringify( this, 3, null, 2 )};
        this.model.insertObject( data_config, this ); } // xtra line of code, but more readable

    logUpdate( message : string ) {
        if ( !this.object_view_id ) {  console.log( "*** ERROR: object needs an id to log. ***" ); return; }
        if ( message.includes( "ERROR" )) { 
            this.monitorLed.setFail( message );
        } else if( message.includes( "finished" )) {
            this.monitorLed.setPass( message );
        } else { 
            this.monitorLed.setLedText( message ); }
        this.logObjects.push( this.logObjectFactory.createLogObject( message, this                   ));
        const data_config = { object_view_id: this.object_view_id, object_data: this.stringifier.stringify( this, 3, null, 2 )};
        this.model.updateObject( data_config, this                                                   ); }
    
    
    processQueryResult( _event: any, results: { data: string | any[]; } ) { if ( results.data.length > 0 ) { console.log( results.data ); }}
    getObjectViewId() { return this.object_view_id; }
}
```
```typescript
start() {
        // this.logUpdate( "monitor led component starting..." );
        let object_being_monitored = this.$host.getAttribute( "monitored_object_id"  ) as string;
        let source_query_config = { object_view_id: object_being_monitored, object_data: {}};
        let model               = new Model( new SourceData({ Runner: FetchRunner, url: this.data_source_location! }));
        setInterval(() => { model.selectObject( source_query_config, this ); }, 2500 ); }
```
```typescript
class MonitoredObjectsTableSelector {
    constructor() { console.log( 'constructing MonitoredObjectsTableSelector object...' ); }

    public selectMonitoredObject( objectViewIdArg: string ): void {
        console.log( "selecting monitored object..." );
        const query = `select object_data from monitored_objects where object_view_id='${ objectViewIdArg }'`;
    }
    
}
```
```typescript
class LogObject implements IWebComponent {

    timestamp  :number =  0;
    method     :string = "";
    message    :string = "";
    
    $log_object_container !:HTMLElement;

    setMessage( message_arg :string ){ this.message = message_arg; }

    static observedAttributes(){} // return Array<String> of attributes you want to observe

    constructor( private $el: HTMLElement, private $host: Element ) {} // $el is the shadowRoot at this point
    
    cloneMe() { return this.$el.cloneNode( false ); }

    /**
     * Invoked each time the custom element is appended into a document-connected element.
     * This will happen each time the node is moved, and may happen before the element's contents have been fully parsed.
     */
    connectedCallback() {
        console.log( 'defining log-object inner html...' );
        this.$log_object_container = this.$el.querySelector( ".log-object-container" )!;
        this.$log_object_container.querySelector( ".timestamp" )!.innerHTML = this.timestamp.toString();
        this.$log_object_container.querySelector( ".method"    )!.innerHTML = this.method;
        this.$log_object_container.querySelector( ".message"   )!.innerHTML = this.message;
    }

    /** Invoked each time the custom element is disconnected from the document's DOM. */
    disconnectedCallback() { console.log( 'log-object disconnected' ); }
    adoptedCallback() {      console.log( 'log-object moved'        ); }

    /**
     * Invoked each time one of the custom element's attributes is added, removed, or changed.
     * Which attributes to notice change for is specified in a static get observedAttributes method
     *
     * @param name
     * @param oldValue
     * @param newValue
     */
    attributeChangedCallback(name: string, oldValue: any, newValue: any ) {
        const nameProp = name.replace( /-[a-zA-Z]/g, ( found: string) => found.slice(1).toUpperCase());
        ( this as any )[ nameProp ] = newValue;
    }
}
```
```typescript
()=>import('./log-object.component')
```
```typescript
() => customElements.define('log-object', wrap(()=>import('./log-object.component'), 'LogObject', observedAttributesLogObject))
```
```typescript
createObjectRow ( object_id: string ): void {
        const nextFunction = "checkResults";
        // create a new row in the monitored objects table  
    }
```
```typescript
updateQue() {
        const freshData = this.logObjectContainer.getLogObjects();
        for ( const logObject in freshData ) {
            this.addLog( freshData[ logObject ]); }}
```
```typescript
() => customElements.define('log-viewer', wrap(()=>import('./log-viewer.component'), 'LogViewer', observedAttributesLogViewer))
```
```typescript
class MonitoredObjectsTableInserter {

    constructor() { console.log( 'constructing MonitoredObjectsTableInserter object...' ); }
    queryInsertProcessor = new QueryInsertProcessor();
    insertMonitoredObject ( object_view_id: string, object_data: string ): void {
        const args: IApiArgs  = {
            query: "insert into monitored_objects( object_view_id, object_data ) values ( '"
                + object_view_id + "', '" + object_data + "' )",
            data: {},
            queryResultProcessor: this.queryInsertProcessor
        }
        console.log( "running query: " + args.query );
        // this.dataSource.runQuery( args );
    }
}
```
```typescript
class LogObjectProcessor  {
    logObjectContainer: LogObjectContainer;
    writtenLogs:   Array< ILogObject > = [];
    unwrittenLogs: Array< ILogObject > = [];

    constructor( logObjectContainerArg: LogObjectContainer ) {
        // console.log( 'constructing LogObjectProcessor object...' );
        this.logObjectContainer = logObjectContainerArg; }

    updateQue() {
        const freshData = this.logObjectContainer.getLogObjects();
        for ( const logObject in freshData ) {
            this.addLog( freshData[ logObject ]); }}

    addLog( logToAdd: ILogObject ): void {
        if ( !FreshToolBox.isInArray( logToAdd, this.writtenLogs )) {
                this.unwrittenLogs.push( logToAdd ); }}

    processLogObjects(): void {
        for ( const logObject in this.unwrittenLogs ) {
            this.writtenLogs.push( this.unwrittenLogs[ logObject ]); }
        this.unwrittenLogs = []; }

    getWrittenLogs(): Array< ILogObject > {
        return this.writtenLogs; }

    getUnwrittenLogs(): Array< ILogObject > {
        return this.unwrittenLogs; }

    clearLogs(): void {
        this.writtenLogs = [];
        this.unwrittenLogs = [];
        this.logObjectContainer.clearLogs(); }
}
```
```typescript
class MonitorLed implements IWebComponent, IQueryResultProcessor {
    monitored_object_id  = "";
    data_source_location :string | null = "";
    monitor_led_data     :ServerLedData = new ServerLedData();

    // return an array containing the names of the attributes you want to observe.  Not sure why this is here yet.
    static observedAttributes () {}

    constructor( private $el: HTMLElement, private $host: Element ) {
        this.data_source_location = $host.getAttribute( "data_source_location" ) as string; }

    /**
     * Invoked each time the custom element is appended into a document-connected element.
     * This will happen each time the node is moved, and may happen before the element's contents have been fully parsed.
     */
    connectedCallback () {
        // this.logUpdate( 'monitor-led connected' );
        this.render().start();
    }

    render() { 
        this.$el.innerHTML = `
        <div class="monitor-led">${ this.monitor_led_data.ledText }</div>
        `;
        let monitor_led = this.$el.querySelector< HTMLElement >( '.monitor-led' ); 
        monitor_led!.style.backgroundColor = this.monitor_led_data.classObject.background_color;
        monitor_led!.style.textAlign       = this.monitor_led_data.classObject.text_align;
        monitor_led!.style.marginTop       = this.monitor_led_data.classObject.margin_top;
        monitor_led!.style.color           = this.monitor_led_data.classObject.color;
        return this;
    }

    /** Invoked each time the custom element is disconnected from the document's DOM. */
    disconnectedCallback () { console.log( 'monitor-led disconnected' ); }

    /** Invoked each time the custom element is moved to a new document. */
    adoptedCallback () {  console.log( 'monitor-led moved' ); }

    /**
     * Invoked each time one of the custom element's attributes is added, removed, or changed.
     * Which attributes to notice change for is specified in a static get observedAttributes method
     *
     * @param name
     * @param oldValue
     * @param newValue
     */
    attributeChangedCallback ( name: string, oldValue: any, newValue: any ) {
        const nameProp = name.replace( /-[a-zA-Z]/g, ( found: string ) => found.slice( 1 ).toUpperCase() );
        ( this as any )[ nameProp ] = newValue;
    }

    start() {
        // this.logUpdate( "monitor led component starting..." );
        let object_being_monitored = this.$host.getAttribute( "monitored_object_id"  ) as string;
        let source_query_config = { object_view_id: object_being_monitored, object_data: {}};
        let model               = new Model( new SourceData({ Runner: FetchRunner, url: this.data_source_location! }));
        setInterval(() => { model.selectObject( source_query_config, this ); }, 2500 ); }

    processQueryResult( callbackObject: MonitorLed, query_result: any ) {
        if( query_result.length < 15 || !JSON.parse( query_result ).object_data ) { return; }
        let data = JSON.parse( JSON.parse( query_result ).object_data );
        if ( Object.keys(data).length === 0 ) { 
            this.render();
            return; }
        this.monitor_led_data = data.monitorLed;
        this.render();
        let object_being_monitored = this.$host.getAttribute( "monitored_object_id"  ) as string;
        let the_number_part = object_being_monitored.match( /\d+/ )![0]!;
        let the_name_part   = object_being_monitored.replace( "_" + the_number_part, ""); 
        const event_name = "event-" + this.kebabize( the_name_part ) + "-" + the_number_part;
        data.noisy_component = this;
        let led_event = new CustomEvent( event_name, { bubbles: true, detail: data });
        document.dispatchEvent( led_event); }
    
    kebabize( str: string ) {
        return str.split('').map((letter, idx) => {
            return letter.toUpperCase() === letter
            ? `${idx !== 0 ? '-' : ''}${letter.toLowerCase()}`
            : letter;
    }).join(''); }
}
```
```typescript
start() {
        setInterval(() => { 
            // console.log( "refreshing logs... " );
            this.logObjectContainerSource.refresh();
            this.logs = this.logObjectContainerSource.logObjectProcessor.getWrittenLogs(); }, 1000 ); }
```
```typescript
constructor() {
        this.classObject   = new MonitorLedClassObject();
        this.ledText       = "ready.";
        this.RUNNING_COLOR = "lightyellow";
        this.PASS_COLOR    = "lightgreen";
        this.FAIL_COLOR    = "#fb6666"; // lightred is not understood by CSS.  Whaaa... ??
    }
```
```typescript
class TableManager {
    // dataSource: IDataObject;
    subjects: Array< ISubject > = [];

    constructor() {
        // this.dataSource = DataSourceFactory.getDataSource();
    }

    createObjectRow ( object_id: string ): void {
        const nextFunction = "checkResults";
        // create a new row in the monitored objects table  
    }

    checkResults (
        _event: unknown,
        results: { data: { error: string | string[] }; query: string }
    ): void {
        console.log(
            "checking results of table manager inserting new object row... "
        );
        if ( results.data.error ) {
            if ( results.data.error.includes( "Duplicate entry" ) ) {
                console.log(
                    "*** WARNING: duplicate entry in monitored objects table. ***"
                );
            } else {
                console.error(
                    "*** ERROR: while running query: " + results.query + " ***"
                );
            }
        }
    }
}
```
```typescript
constructor() { console.log( 'constructing MonitoredObjectsTableSelector object...' ); }
```
```typescript
log_object => {
            let formatted_time_stamp = new Date( log_object?.timestamp ).toLocaleString()
            let li_inner_html = `
                <div class="log-object-container">
                    <div class="timestamp">${ formatted_time_stamp }</div>
                    <div class="method"   >${ log_object.method    }</div>
                    <div class="message"  >${ log_object.message   }</div>
                </div>`;
            let $new_list_element = document.createElement( 'li' );
            $new_list_element.innerHTML = li_inner_html;
            this.$list_of_log_objects.appendChild( $new_list_element );
        }
```
```typescript
()=>import( './components/log-object/log-object.component'               )
```
```typescript
class LogObjectContainer {
    logObjects: Array< ILogObject > = [];
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    constructor() {}

    addLog( logToAdd: ILogObject ): void {
        if ( !FreshToolBox.isInArray( logToAdd, this.logObjects )) {
            this.logObjects.push( logToAdd ); }}

    getLogObjects(): Array< ILogObject > { return this.logObjects; }

    clearLogs(): void { this.logObjects = []; }
}
```
```typescript
class MonitorLedClassObject {
    background_color: string;
    text_align: string;
    margin_top: string;
    color: string;

    constructor() {
        this.background_color = "lightyellow";
        this.text_align       = "left";
        this.margin_top       = "2px";
        this.color            = "black"; }
}
```
```typescript
logUpdate( message : string ) {
        if ( !this.object_view_id ) {  console.log( "*** ERROR: object needs an id to log. ***" ); return; }
        if ( message.includes( "ERROR" )) { 
            this.monitorLed.setFail( message );
        } else if( message.includes( "finished" )) {
            this.monitorLed.setPass( message );
        } else { 
            this.monitorLed.setLedText( message ); }
        this.logObjects.push( this.logObjectFactory.createLogObject( message, this                   ));
        const data_config = { object_view_id: this.object_view_id, object_data: this.stringifier.stringify( this, 3, null, 2 )};
        this.model.updateObject( data_config, this                                                   ); }
```
```typescript
getLogObjects(): Array< ILogObject > { return this.logObjects; }
```
```typescript
class MonitoredObjectsTableUpdater {    
    constructor() { console.log( 'constructing MonitoredObjectsTableUpdater object...' ); }
    
    /**
     *  @method update
     *  @description
     *  
     *  Stringifies the passed in Subject and updates the monitored_objects table with this information.
     * 
     *  @param {ISubject} subject The subject to be stringified.
     *      
     *  @param {string} objectViewIdArg This is needed to locate the correct object in the table that will be updated.
     *  @return {*}  {void}
     *  @memberof MonitoredObjectsTableUpdater
     */
    public update( subject: ISubject, objectViewIdArg: string ): void {
        console.log( "updating table..." );
        if ( !objectViewIdArg  ) { console.log( "*** ERROR: no id sent to update method! ***" ); return; }
        const query = "update monitored_objects set object_data='" + JSON.stringify( subject ) + 
                      "' where object_view_id='" + objectViewIdArg + "'";

        console.log( `running query${ query }...` ); }
}
```
```typescript
() => { 
            // console.log( "refreshing logs... " );
            this.logObjectContainerSource.refresh();
            this.logs = this.logObjectContainerSource.logObjectProcessor.getWrittenLogs(); }
```
```typescript
()=>import('./log-viewer.component')
```
```typescript
constructor( config: { new_id: string | null, data_source_location: string | null; } ) {
        if ( config.new_id?.length === 0 ) { config.new_id = Math.floor( Math.random() * 1000 + 1000 ).toString(); }
        if ( config.new_id?.includes('_')) {
            this.object_view_id = config.new_id
        } else { this.object_view_id = `${ this.constructor.name }_${ config.new_id }`; }
        this.logObjectFactory  = new LogObjectFactory();
        this.logObjects        = [ this.logObjectFactory.createLogObject( "constructing...", this )];
        if ( config.data_source_location?.length === 0 && document.querySelector( '.data-source-location' )) { 
            config.data_source_location = document.querySelector( '.data-source-location' )?.innerHTML || "" }
        this.model             = new Model( new SourceData({ Runner: FetchRunner, url: config.data_source_location! }));
        this.monitorLed        = new MonitorLed();
        this.stringifier       = new Stringifier();
        const data_config        = { object_view_id: this.object_view_id, object_data: this.stringifier.stringify( this, 3, null, 2 )};
        this.model.insertObject( data_config, this ); } // xtra line of code, but more readable
```
```typescript
class MonitorLed {
    classObject:   MonitorLedClassObject;
    ledText:       string;
    RUNNING_COLOR: string;
    PASS_COLOR:    string;
    FAIL_COLOR:    string;
    constructor() {
        this.classObject   = new MonitorLedClassObject();
        this.ledText       = "ready.";
        this.RUNNING_COLOR = "lightyellow";
        this.PASS_COLOR    = "lightgreen";
        this.FAIL_COLOR    = "#fb6666"; // lightred is not understood by CSS.  Whaaa... ??
    }

    setFail( fail_message : string ) {
        this.setLedBackgroundColor( this.FAIL_COLOR );
        this.setLedTextColor(       "white"         );
        this.setLedText(            fail_message    ); }
    
    setPass( pass_message : string ) {
        this.setLedBackgroundColor( this.PASS_COLOR );
        this.setLedTextColor(       "black"         );
        this.setLedText(            pass_message    ); }

    setLedBackgroundColor( newColor : string ) { this.classObject.background_color = newColor; }
    setLedTextColor(       newColor : string ) { this.classObject.color            = newColor; }
    setLedText(            newText  : string ) { this.ledText                      = newText ; }
}
```
```typescript
interface IMonitoredObject { logUpdate( textToLog: string ): void; }
```
```typescript
set logs( logObjects: ILogObject[]) {
        // console.log('prop written, new value', logObjects );
        if ( logObjects.length !== this.log_length ) { 
            console.log( "length changed! "); 
            this.log_length = logObjects.length;
            this.displayLogObjects( logObjects, this );
        }
    }
```
```typescript
public selectMonitoredObject( objectViewIdArg: string ): void {
        console.log( "selecting monitored object..." );
        const query = `select object_data from monitored_objects where object_view_id='${ objectViewIdArg }'`;
    }
```
```typescript
constructor() { console.log( 'constructing MonitoredObjectsTableUpdater object...' ); }
```
```typescript
constructor() { console.log( 'constructing MonitoredObjectsTableInserter object...' ); }
```
```typescript
connectedCallback() {
        console.log( 'defining log-object inner html...' );
        this.$log_object_container = this.$el.querySelector( ".log-object-container" )!;
        this.$log_object_container.querySelector( ".timestamp" )!.innerHTML = this.timestamp.toString();
        this.$log_object_container.querySelector( ".method"    )!.innerHTML = this.method;
        this.$log_object_container.querySelector( ".message"   )!.innerHTML = this.message;
    }
```
```typescript
class DataObjectLogger extends MonitoredObject {

	constructor( config :IMonitoredObjectConfig ) { super( config ); }
	
    static capitalizeFirstLetter ( stringToUppercase: string ): string {
        return stringToUppercase.charAt( 0 ).toUpperCase() + stringToUppercase.slice( 1 ); }

    static isInArray ( objectToSearchFor: any, arrayToSearch: Array< any > ): boolean {
        return( arrayToSearch.indexOf( objectToSearchFor ) > -1 ); }
    
    static assert( condition: any, msg?: string ): asserts condition {
        if ( !condition ) {
            throw new Error( msg )
        }}
}
```
```typescript
class LogObjectContainerSource implements IQueryResultProcessor {
    logObjectContainer: LogObjectContainer;
    logObjectProcessor: LogObjectProcessor;
    model: Model;
    config: ISourceConfig
    source_query_config: ISourceQueryConfig;
    constructor( _config: ISourceConfig ) {
        this.config = _config;
        this.logObjectContainer = new LogObjectContainer();
        this.logObjectProcessor = new LogObjectProcessor( this.logObjectContainer );
        this.model = new Model( new SourceData({ Runner: FetchRunner, url: _config.location }));
        this.source_query_config = { object_view_id: _config.object_id, object_data: {}}; }

    getWrittenLogs () { return this.logObjectProcessor.getWrittenLogs(); }

    refresh() {
        if ( this.config.type === "url" ) {
            this.refreshFromDatabase();
        } else if ( this.config.type === "file" ) {
            this.refreshFromFile( this.config.location );
        }}

    refreshFromDatabase() { this.model.selectObject( this.source_query_config, this ); }

    processQueryResult( resultProcessor: LogObjectContainerSource, result: any ) {
        if( result.length  == 0  || result.trim() == "null" ) { return; }
        let object_data;
        try {
            object_data = JSON.parse( JSON.parse( result ).object_data );
        } catch ( error ) {
            console.error( error );
            return;
        }
        const logObjects = object_data.logObjects;
        for ( const logObject of logObjects ) {
            resultProcessor.logObjectContainer.addLog( logObject ); }
        resultProcessor.logObjectProcessor.updateQue();
        resultProcessor.logObjectProcessor.processLogObjects(); }

    refreshFromFile( file_path: string ) {
        fetch( file_path )
            .then( response => response.text() )
            .then( text => {
                text = text.split( '\r' ).join( '' ); // if performance is an issue, change this maybe.
                const file_array = text.split( "\n" );
                const log_objects: ILogObject[] = [];
                let parsed_line: ILogObject = { id: "", timestamp: 0, message: "", method: "" };
                for ( const line of file_array ) {
                    if ( line.length > 0 ) {
                        try {
                            parsed_line = JSON.parse( line );
                        } catch ( error ) {
                            console.error( "error parsing line: " + line );
                        }
                        log_objects.push( parsed_line );
                    }
                }
                for ( const logObject of log_objects ) {
                    this.logObjectContainer.addLog( logObject );
                }
                this.logObjectProcessor.updateQue();         // from log object container to internal Q
                this.logObjectProcessor.processLogObjects(); // from internal Q to written log objects
            });
    }
}
```
```typescript
text => {
                text = text.split( '\r' ).join( '' ); // if performance is an issue, change this maybe.
                const file_array = text.split( "\n" );
                const log_objects: ILogObject[] = [];
                let parsed_line: ILogObject = { id: "", timestamp: 0, message: "", method: "" };
                for ( const line of file_array ) {
                    if ( line.length > 0 ) {
                        try {
                            parsed_line = JSON.parse( line );
                        } catch ( error ) {
                            console.error( "error parsing line: " + line );
                        }
                        log_objects.push( parsed_line );
                    }
                }
                for ( const logObject of log_objects ) {
                    this.logObjectContainer.addLog( logObject );
                }
                this.logObjectProcessor.updateQue();         // from log object container to internal Q
                this.logObjectProcessor.processLogObjects(); // from internal Q to written log objects
            }
```
```typescript
()=>import( './components/log-viewer/log-viewer.component'               )
```

## gpt 4.5 response
https://chatgpt.com/share/67d5e6cf-a070-8006-8528-ed5c4cfc5a86
