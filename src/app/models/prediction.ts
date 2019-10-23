export class Prediction{
    name : string;
    toString():string{
        return `${this.name}`;
    }

    constructor(name:string){
        this.name = name;
    }
}