package top.singu.entity;

import java.io.Serializable;

public class Data implements Serializable {
	
	private Boolean status;
	private Integer code;
	private String message;
	private Object data;
	private String dataType;
	
	public Data( ) {
		super( );
	}
	
	public Data( Boolean status, Integer code, String message, Object data, String dataType ) {
		super( );
		this.status = status;
		this.code = code;
		this.message = message;
		this.data = data;
		this.dataType = dataType;
	}
	
	public Boolean getStatus( ) {
		return status;
	}
	
	public void setStatus( Boolean status ) {
		this.status = status;
	}
	
	public Integer getCode( ) {
		return code;
	}
	
	public void setCode( Integer code ) {
		this.code = code;
	}
	
	public String getMessage( ) {
		return message;
	}
	
	public void setMessage( String message ) {
		this.message = message;
	}
	
	public Object getData( ) {
		return data;
	}
	
	public void setData( Object data ) {
		this.data = data;
	}
	
	public String getDataType( ) {
		return dataType;
	}
	
	public void setDataType( String dataType ) {
		this.dataType = dataType;
	}
	
	@Override
	public String toString( ) {
		return "Data{" + "status=" + status + ", code=" + code + ", message='" + message + '\'' + ", data=" + data + ", dataType='" + dataType + '\'' + '}';
	}
}
