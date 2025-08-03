import grpc
import calmbot_pb2
import calmbot_pb2_grpc

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = calmbot_pb2_grpc.CalmbotServiceStub(channel)

    # Test LogMood
    mood_res = stub.LogMood(
        calmbot_pb2.LogMoodRequest(user_id='user123', mood='happiness')
    )
    print('LogMood reply:', mood_res.reply)

    # Test Chat
    chat_res = stub.Chat(
        calmbot_pb2.ChatRequest(user_id='user123', message='Hello CalmBot!')
    )
    print('Chat reply:', chat_res.reply)

    # Test SaveJournal
    journal_res = stub.SaveJournal(
        calmbot_pb2.JournalRequest(user_id='user123', mood='sadness', entry='Testing journaling')
    )
    print('Journal reply:', journal_res.reply)

    # Test GetProgress
    prog_res = stub.GetProgress(
        calmbot_pb2.ProgressRequest(user_id='user123')
    )
    print('Progress summary:', prog_res.summary)

if __name__ == '__main__':
    main()