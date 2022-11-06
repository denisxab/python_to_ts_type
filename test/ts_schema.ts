export interface ClientsWbsRequest{
/*AUTO_GEN:2022-11-06 13:07:45.917090

    Запрос клиента, для сервера
    	
*/
	//  Модификации для запроса.
	mod:ClientsWbsRequest_Mod|ClientsWbsRequest_ModAlternatives;
	//  Нужен для того чтобы можно было разными способами обрабатывать ответ на

	//  стороне клиента.
	h_id:number;
	//  Идентификатор команды, нужен если используется асинхронность
	uid_c:number;
	//  Тело запроса
	body:ClientsWbsRequest_ExeCommand|ClientsWbsRequest_GetInfoServer|ClientsWbsRequest_ImportFromServer|ClientsWbsRequest_CreateSubscribe|ClientsWbsRequest_AllowedFunc;
	//  Время отправки сообщения от клиента в UNIX формате.
	t_send:number;
}
export enum WbsResponseCode{
/*AUTO_GEN:2022-11-06 13:07:45.917176

    Список кодов ответа
    	
*/
	//  Ошибка валидации запроса от клиента
	error_parse_request_clients =  100,
	//  Ошибка выполнения команды на стороне сервера
	error_server =  101,
	//  Ошибка аутентификации по токену
	token_error =  102,
	//  Успешное выполнение
	ok =  200,
	//  Сообщение в качестве уведомления
	notify =  201,
	//  Произошел откат транзакции, по причине клиента(например превышено время ожидания ответа)
	rollback_from_clients =  401,
	//  Произошел откат транзакции, по причине сервера
	rollback_from_server =  402,
}
export interface ServerWbsResponse{
/*AUTO_GEN:2022-11-06 13:07:45.917185

    Ответ от сервера, для клиента
    	
*/
	//  Нужен для того чтобы можно было разными способами обрабатывать ответ на

	//  стороне клиента.
	h_id:number;
	//  Идентификатор команды, нужен если используется асинхронность
	uid_c:number;
	//  Код ответа
	code:WbsResponseCode;
	//  Время отправки сообщения от клиента в UNIX формате.
	t_send:number;
	//  Время выполнения(t_send из запроса - t_send из ответа), заполняется на

	//  стороне клиента.
	t_exec:number;
	//  Текст ошибки
	error:string;
	//  Ответ
	response:string;
}
