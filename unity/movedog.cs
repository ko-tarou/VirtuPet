using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class MoveDog : MonoBehaviour
{
    public Transform[] goals; // 巡回地点の配列
    private int destNum = 0; // 現在の目的地のインデックス
    private NavMeshAgent agent; // NavMeshAgentコンポーネント
    public float rotationSpeed = 5f; // 回転速度
    public float moveSpeed = 2.0f; // 移動速度

    void Start()
    {
        // NavMeshAgentを取得
        agent = GetComponent<NavMeshAgent>();

        // NavMeshAgentの速度を設定
        agent.speed = moveSpeed;

        // 最初の巡回地点を設定
        if (goals.Length > 0)
        {
            SetRandomGoal();
        }
        else
        {
            Debug.LogWarning("巡回地点が設定されていません。");
        }
    }

    void Update()
    {
        // 向きの調整（目的地を向く）
        if (agent.hasPath)
        {
            Vector3 direction = agent.steeringTarget - transform.position; // 次の移動ターゲットの方向
            Quaternion targetRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, rotationSpeed * Time.deltaTime);
        }

        // 目的地に到達したら次の巡回地点を設定
        if (!agent.pathPending && agent.remainingDistance < 0.5f)
        {
            SetRandomGoal();
        }
    }

    void SetRandomGoal()
    {
        int previousDest = destNum;

        // ランダムに次の巡回地点を選択（現在の地点と同じ場所を避ける）
        do
        {
            destNum = Random.Range(0, goals.Length);
        } while (destNum == previousDest);

        // 次の目的地を設定
        agent.destination = goals[destNum].position;

        // デバッグ用に現在の目的地を出力
        Debug.Log("次の巡回地点: " + destNum);
    }
}
