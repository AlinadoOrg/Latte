package top.singu.entity;

public class TextContext {
	
	public final String dataType = "TextContext";
	
	private String context;
	
	public TextContext( ) {
		super( );
		this.context = "抱歉，我无法理解你说的话";
	}
	
	public TextContext( String context ) {
		this.context = context;
	}
	
	public String getContext( ) {
		return context;
	}
	
	public void setContext( String context ) {
		this.context = context;
	}
	
	@Override
	public String toString( ) {
		return "TextContext{" + "context='" + context + '\'' + '}';
	}
}
