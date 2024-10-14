class SymbolTable{
    constructor(){
        this.table=new Map()
    }
}

//adding a symbol
function addSymbol(jina,type,value,scope="global") {
    if(this.table.has(jina)){
        throw newError('${jina} already exists')
    }
     this.table.set(jina,{type,value,scope});
   }


   //updating a symbol

function updateSymbol(jina,newJina){
    if(!this.table.has(jina)){
        throw new Error(`Symbol "${jina}" already exists `)
    }
    let symbol=this.table.get(jina);
    symbol.value=newValue;
    this.table.set(jina,symbol);
}
//getting a symbol
function getSymbol(name){
    if(!this.table.has(name)){
        throw new Error("The symbol is not found")
    }
    return this.table.get(name);
}


//cheching if a symbol exixts

function hasSymbol(jina){
    return this.table(jina)
    
}


function printTable(){
    console.log("Symbol table")

    this.table.forEach((value,key) => {
        console.log(`${key}:`,value);
    });
}