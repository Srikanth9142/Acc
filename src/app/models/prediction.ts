export class Prediction{
    name : string;

    toString():string{
        return `Your Accent is:${this.name}`;
    }

    constructor(name:string){
        this.name = name;
    }
}